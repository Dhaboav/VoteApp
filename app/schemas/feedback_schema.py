"""Feedback schema for user feedback submission."""

from pydantic import BaseModel


class Feedback(BaseModel):
    """Schema for user feedback submission."""

    detail: str
