"""
Pydantic model for the User database table.

Used for database CRUD operations in the application.
"""

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Pydantic schema for User base attributes."""

    email: EmailStr
    username: str
    fullname: str


class UserCreate(UserBase):
    """Pydantic schema for creating a new User."""

    password: str
