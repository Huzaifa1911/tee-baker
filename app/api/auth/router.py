from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from ...core.database import SessionDep
from .schemas import UserPublic, Token
from .service import auth_service
from .utils import create_access_token
from ..deps import CurrentUser


router = APIRouter(
    prefix="/auth",
)


@router.post("/access-token")
async def login_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = auth_service.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return Token(
        access_token=create_access_token(user.id),
    )


@router.get("/verify-token", response_model=UserPublic)
async def verify_access_token(current_user: CurrentUser) -> UserPublic:
    """
    Verify token and return current logged in user
    """
    return current_user
