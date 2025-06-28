"""
SQLModel to represent Users entity.

This module are used for data modeling of Users in the database.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, func


class Users(SQLModel, table=True):
    """
    sqlmodel to represent Users entity.

    Attributes:
        id (UUID): The unique identifier for the user.
        email (str): The email address of the user.
        username (str): The username of the user.
        password (str): The password of the user.
        created_at (datetime): Timestamp of user creation.
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    username: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: Optional[datetime] = Field(
        default=None, sa_column_kwargs={"server_default": func.now()}
    )
