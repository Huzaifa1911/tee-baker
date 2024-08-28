from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from datetime import date


class GenderEnum(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"


class UserBase(BaseModel):
    full_name: str
    user_name: str
    email: EmailStr
    gender: list[GenderEnum]
    dob: date
    bio: Optional[str]
    profile_url: Optional[str]


class UserCreate(UserBase):
    pass
