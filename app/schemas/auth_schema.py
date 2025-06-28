"""Schema for user login token."""

from pydantic import BaseModel


class TokenSchema(BaseModel):
    """Schema for user login token."""

    access_token: str
    token_type: str = "bearer"
