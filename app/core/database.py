from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Annotated
from fastapi import Depends
from collections.abc import Generator

from .config import api_settings

engine = create_engine(url=str(api_settings.SQLALCHEMY_DATABASE_URI))
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db_session = sessionmaker(autoflush=False, bind=engine)()
    try:
        yield db_session
    finally:
        db_session.close()


SessionDep = Annotated[Session, Depends(get_db)]


def init_db(session: SessionDep) -> None:
    pass
