from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from ...core.database import SessionDep
from .schemas import UserPublic, Token, UserCreate
from .service import AuthService
from .utils import create_access_token
from ..deps import CurrentUser
from ...core.config import api_settings
from ...core.exceptions.common import ResourceNotFoundException


router = APIRouter(prefix="/auth")


@router.post("/access-token")
async def login_access_token(
    *,
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = AuthService.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )

    if not user:
        raise ResourceNotFoundException(
            id=form_data.username,
            resourceType="User",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return Token(
        access_token=create_access_token(user.id),
    )


@router.get("/verify-token", response_model=UserPublic)
async def verify_access_token(*, current_user: CurrentUser) -> UserPublic:
    """
    Verify token and return current logged in user
    """
    return current_user


@router.post("/signup", response_model=UserCreate)
async def singup_user(*, session: SessionDep, user_in: UserCreate) -> UserCreate:
    """
    Create new user
    """
    user = AuthService.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    user = AuthService.create_user(session=session, user_create=user_in)
    # Send an email to user
    if api_settings.emails_enabled and user_in.email:
        # send email to user
        pass

    # return Token(access_token=create_access_token(user.id))
    return user_in
