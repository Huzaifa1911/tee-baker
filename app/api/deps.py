import jwt
from jwt.exceptions import JWSDecodeError
from pydantic import ValidationError
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from ..core.database import SessionDep
from ..core.config import api_settings
from .auth.utils import ALGORITHM
from .auth.models import User
from .auth.schemas import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{api_settings.API_V1_STR}/access-token"
)

TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(
    session: SessionDep,
    token: TokenDep,
):
    try:
        payload = jwt.decode(token, api_settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)

    except (JWSDecodeError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = session.get(User, token_data.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive User"
        )

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )

    return current_user
