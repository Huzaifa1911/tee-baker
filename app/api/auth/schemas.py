from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
import uuid
from datetime import date

from ...core.schemas.enums import GenderEnum


# Shared properties
class UserBase(BaseModel):
    full_name: str
    user_name: str
    email: EmailStr
    gender: GenderEnum
    dob: date
    bio: str | None = None
    profile_url: str | None = None
    is_active: bool = True
    is_super: bool = False


# Properties to receive via API on create
class UserCreate(UserBase):
    password: str


# Properties to recevie via API on update
class UserUpdate(UserBase):
    full_name: str | None
    user_name: str | None
    email: EmailStr | None
    gender: GenderEnum | None
    dob: date | None


# Properties to receive via API on password reset
class UpdatePassword(BaseModel):
    current_password: str
    new_password: str


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    created_at: date
    updated_at: date


class UsersPublic(BaseModel):
    data: list[UserPublic]
    count: int


# JSON payload containing access token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(BaseModel):
    sub: str | None = None
