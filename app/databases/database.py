"""
Database setup and session management for SQLite.

- Configures the database engine using `sqlite` driver.
- Creates a sessionmaker for ORM operations.
- Provides a generator dependency to yield database sessions.

The `DATABASE_URL` variable controls the SQLite file location.
"""

from typing import Annotated, Generator

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = f"sqlite:///./storage/app.db"
engine = create_engine(DATABASE_URL)


def create_all_tables() -> None:
    SQLModel.metadata.create_all(engine)


def close_db() -> None:
    engine.dispose()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.

    Yields:
        Session: A SQLModel session for database operations.
    """
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


SessionDep = Annotated[Session, Depends(get_db)]
