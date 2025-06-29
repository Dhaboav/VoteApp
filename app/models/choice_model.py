"""
SQLModel for representing the Choice entity.

This module defines the data model for a Choice, which is associated with an Event.
"""

import uuid
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Choice(SQLModel, table=True):
    """
    SQLModel representing the Choice entity.

    Attributes:
        id (int)        : The primary key for the choice.
        choice (str)    : The text of the choice option.
        event_id (UUID) : The foreign key linking to the associated event.

    Relationships:
        event (Event)       : The event to which this choice belongs.
        votes (List[Vote])  : A list of vote associated with the event and user.
    """

    id: int = Field(default=None, primary_key=True)
    choice: str = Field(nullable=False)

    event_id: uuid.UUID = Field(foreign_key="event.id", nullable=False)

    event: Optional["Event"] = Relationship(back_populates="choices")  # type: ignore
    votes: List["Vote"] = Relationship(back_populates="choice")  # type: ignore
