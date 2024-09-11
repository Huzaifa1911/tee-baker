from pydantic import EmailStr
from sqlalchemy.orm import Session
import sqlalchemy as sa

from .models import User
from .utils import verify_password, get_password_hash
from .schemas import UserCreate


class AuthService:

    @staticmethod
    def authenticate(
        *, session: Session, email: EmailStr, password: str
    ) -> User | None:
        user = AuthService.get_user_by_email(session=session, email=email)

        if not user:
            return None

        if not verify_password(plain_password=password):
            return None

        return user

    @staticmethod
    def get_user_by_email(*, session: Session, email: EmailStr) -> User | None:
        stmt = sa.select(User).where(User.email == email)
        session_user = session.execute(statement=stmt).first()
        return session_user

    @staticmethod
    def create_user(*, session: Session, user_create: UserCreate) -> UserCreate:
        user_create.password = get_password_hash(user_create.password)
        db_user = User(**user_create.model_dump())
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
