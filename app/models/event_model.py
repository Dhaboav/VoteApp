"""
SQLModel to represent Event entity.

This module are used for data modeling of Event in the database.
"""

import uuid
from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Event(SQLModel, table=True):
    """
    SQLModel representing the Event entity.

    Attributes:
        id (UUID)                      : The unique identifier for the event.
        title (str)                    : The title of the event.
        desc (Optional[str])           : A description of the event.
        expires_at (Optional[datetime]): The deadline for voting or event expiry.
        creator_id (UUID)              : The UUID of the user who created the event (foreign key)

    Relationships:
        creator (Users)         : The user who created the event.
        choices (List[Choice])  : A list of choices associated with the event.
        votes (List[Vote])      : A list of vote associated with the event and user.
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(nullable=False)
    desc: Optional[str] = Field(default=None)
    expires_at: Optional[datetime] = Field(default=None, nullable=True)

    # Foreign Key
    creator_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)

    # Relationships
    creator: Optional["Users"] = Relationship(back_populates="events")  # type: ignore
    choices: List["Choice"] = Relationship(back_populates="event")  # type: ignore
    votes: List["Vote"] = Relationship(back_populates="event")  # type: ignore
