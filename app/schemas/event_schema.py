"""
Pydantic model for the Event database table.

Used for database CRUD operations in the application.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ChoiceSchema(BaseModel):
    """Pydantic schema for choice attribute"""

    choice: str


class EventCreate(BaseModel):
    """Pydantic schema for creating a new Event."""

    name: str
    description: Optional[str] = None
    choices: List[ChoiceSchema]
    expires_at: Optional[datetime] = None


class EventInfo(BaseModel):
    """Pydantic schema for public Event."""

    title: str
    desc: str
    expires_at: Optional[datetime]
