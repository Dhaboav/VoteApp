"""
Pydantic model for the User database table.

Used for database CRUD operations in the application.
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Pydantic schema for User base attributes."""

    email: EmailStr
    username: str


class UserCreate(UserBase):
    """Pydantic schema for creating a new User."""

    password: str


class UserInfo(UserBase):
    """Pydantic schema for User information."""

    created_at: datetime
