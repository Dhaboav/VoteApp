"""
Dependencies for route usage.

Provides a dependency for JWT token validation.

Features:
- Uses standard HTTP status codes and consistent error handling.

Functions:
- get_current_user: Validates JWT tokens and retrieves the authenticated user.
"""

from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from app.config import config
from app.databases import SessionDep
from app.models import Users
from app.schemas import TokenPayload
from app.services import UserService

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"users/login")
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> Users:
    """
    Checks the validity of a JWT token and retrieves the associated user.

    Args:
        session (SessionDep): Database session dependency.
        token (TokenDep): JWT token dependency.

    Raises:
        HTTPException:
        - 404 Not Found if the user does not exist.
        - 403 Forbidden if the token is invalid.
    """

    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(status_code=403, detail="Could not validate credentials")

    user_id = UUID(token_data.sub)
    user = UserService.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


CurrentUserDep = Annotated[Users, Depends(get_current_user)]
