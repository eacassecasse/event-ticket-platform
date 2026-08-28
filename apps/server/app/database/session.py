from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DATABASE_SQL_ECHO,
    connect_args={
        "connect_timeout": 10,
        "application_name": settings.APP_NAME,
    } if settings.DATABASE_URL.startswith("postgresql") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)

def get_db() -> Generator[Session, None, None]:
    """ Provides a db session for a request and close it aftwards. """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
