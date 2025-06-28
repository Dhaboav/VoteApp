"""Schema for user login token."""

from typing import Optional

from pydantic import BaseModel


class TokenSchema(BaseModel):
    """Schema for user login token."""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Schema for token payload."""

    sub: Optional[str] = None
