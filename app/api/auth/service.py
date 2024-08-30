from pydantic import EmailStr
from sqlalchemy.orm import Session
import sqlalchemy as sa

from .models import User
from .utils import verify_password


class AuthService:
    def __init__(self) -> None:
        pass

    def authenticate(
        self, *, session: Session, email: EmailStr, password: str
    ) -> User | None:
        user = self.get_user_by_email(session=session, email=email)

        if not user:
            return None

        if not verify_password(plain_password=password):
            return None

        return user

    def get_user_by_email(self, *, session: Session, email: EmailStr) -> User | None:
        stmt = sa.select(User).where(User.email == email)
        session_user = session.execute(statement=stmt).first()
        return session_user


auth_service = AuthService()
