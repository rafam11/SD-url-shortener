import jwt
import src.core.constants as cons
from pwdlib.hashers.bcrypt import BcryptHasher
from datetime import datetime, timedelta, timezone
from src.db.utils.settings import settings

hasher = BcryptHasher()

def get_password_hash(
    password: str
) -> str:
    return hasher.hash(password)
    
def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return hasher.verify(plain_password, hashed_password)
    
def create_access_token(
    username: str,
    expires_delta: int | None = None
) -> str:
    expire_minutes = expires_delta if expires_delta else cons.DEFAULT_EXPIRE_JWT_TOKEN
    payload = {
        "sub": username,
        "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=expire_minutes)
    }
    return jwt.encode(
        payload=payload,
        key=settings.secret_key,
        algorithm=cons.HMAC_SHA256_ALGORITHM
    )
