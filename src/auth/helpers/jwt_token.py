import jwt
from datetime import datetime, timedelta, timezone

from src.db.utils.settings import settings


class JwtToken:

    @staticmethod
    def create_access_token(
        username: str,
        expires_delta: timedelta | None = None
    ):
        data = {
            "sub": username
        }
        DEFAULT_EXPIRE_JWT_TOKEN = 15
        expire_time = expires_delta if expires_delta else DEFAULT_EXPIRE_JWT_TOKEN
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=expire_time)
        data["exp"] = expire

        return jwt.encode(
            payload=data,
            key=settings.secret_key,
            algorithm="HS256" 
        )