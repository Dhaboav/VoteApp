"""
SQLModel to represent Event entity.

This module are used for data modeling of Event in the database.
"""

import uuid
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Event(SQLModel, table=True):
    """
    SQLModel representing the Event entity.

    Attributes:
        id (UUID): The unique identifier for the event.
        title (str): The title of the event.
        desc (Optional[str]): A description of the event.
        creator_id (UUID): The UUID of the user who created the event (foreign key).

    Relationships:
        creator (Users): The user who created the event.
        choices (List[Choice]): A list of choices associated with the event.
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(nullable=False)
    desc: Optional[str] = Field(default=None)

    # Foreign Key
    creator_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)

    # Relationships
    creator: Optional["Users"] = Relationship(back_populates="events")  # type: ignore
    choices: List["Choice"] = Relationship(back_populates="event")  # type: ignore
