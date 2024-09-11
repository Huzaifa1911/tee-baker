from sqlalchemy import Column, String, Date, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from ...core.database import Base
from ...core.schemas.enums import GenderEnum
from ...core.models import TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4, unique=True
    )
    full_name = Column(String, nullable=False)
    user_name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    gender = Column(Enum(GenderEnum), nullable=False)
    dob = Column(Date, nullable=False)
    bio = Column(String, nullable=True)
    profile_url = Column(String, nullable=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<User(id={self.id}, full_name={self.full_name}, role={"Super user" if self.is_superuser else "Normal user"})>"
