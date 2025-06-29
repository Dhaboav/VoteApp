"""
SQLModel to represent Vote entity.

This module are used for data modeling of Vote in the database.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint, func


class Vote(SQLModel, table=True):
    """
    SQLModel representing the Vote entity.

    Attributes:
        id (int)                      : The unique identifier for the vote.
        user_id (UUID)                : The foreign key linking to the associated users.
        choice_id (int)               : The foreign key linking to the associated choice.
        event_id (UUID)               : The foreign key linking to the associated event.
        time_logs (Optional[datetime]): Timestamp of user votes.

    Relationships:
        user (Users)    : The event to which this choice belongs.
        choice (Choice) : A list of vote associated with the event and user.
        event (Event)   : A list of vote associated with the event and user.

    Constraints: A user can vote only once per event.
    """

    id: int = Field(default=None, primary_key=True)

    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    choice_id: int = Field(foreign_key="choice.id", nullable=False)
    event_id: uuid.UUID = Field(foreign_key="event.id", nullable=False)

    time_logs: Optional[datetime] = Field(
        default=None, sa_column_kwargs={"server_default": func.now()}
    )

    # Relationships
    user: Optional["Users"] = Relationship(back_populates="votes")  # type: ignore
    choice: Optional["Choice"] = Relationship(back_populates="votes")  # type: ignore
    event: Optional["Event"] = Relationship(back_populates="votes")  # type: ignore

    __table_args__ = (UniqueConstraint("user_id", "event_id", name="uix_user_event"),)
