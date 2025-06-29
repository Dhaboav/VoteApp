"""
SQLModel to represent Users entity.

This module are used for data modeling of Users in the database.
"""

import uuid
from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel, func


class Users(SQLModel, table=True):
    """
    sqlmodel to represent Users entity.

    Attributes:
        id (UUID)            : The unique identifier for the user.
        email (str)          : The email address of the user.
        username (str)       : The username of the user.
        password (str)       : The password of the user.
        created_at (datetime): Timestamp of user creation.

    Relationships:
        event (List[Event]): The event to which this choice belongs.
        votes (List[Vote]) : A list of vote associated with the event and user.
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    username: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: Optional[datetime] = Field(
        default=None, sa_column_kwargs={"server_default": func.now()}
    )

    events: List["Event"] = Relationship(back_populates="creator")  # type: ignore
    votes: List["Vote"] = Relationship(back_populates="user")  # type: ignore
