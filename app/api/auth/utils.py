from datetime import datetime, timedelta, timezone
from typing import Any
import jwt
import bcrypt

from ...core.config import api_settings


ALGORITHM = "HS256"


def create_access_token(subject: str | Any) -> str:
    expires_delta = timedelta(minutes=api_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, api_settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password, bcrypt.gensalt())
