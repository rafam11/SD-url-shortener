from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pwdlib.hashers.bcrypt import BcryptHasher

import app.core.constants as cons
from app.core.config import Settings, get_settings

hasher = BcryptHasher()
auth_headers = HTTPBearer()


def get_password_hash(password: str) -> str:
    return hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hasher.verify(plain_password, hashed_password)


def create_access_token(
    user_id: int, secret_key: str, expires_delta: int | None = None
) -> bytes | str:
    expire_minutes = expires_delta if expires_delta else cons.DEFAULT_EXPIRE_JWT_TOKEN
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=expire_minutes),
    }
    return jwt.encode(
        payload=payload, key=secret_key, algorithm=cons.HMAC_SHA256_ALGORITHM
    )


async def verify_access_token(
    settings: Settings = Depends(get_settings),
    credentials: HTTPAuthorizationCredentials = Depends(auth_headers),
):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            jwt=token, key=settings.secret_key, algorithms=[cons.HMAC_SHA256_ALGORITHM]
        )
        user_id = payload.get("sub")
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credentials cannot be validated.",
            headers={cons.WWW_AUTH_HEADER: cons.BEARER_AUTH},
        )
    return user_id
