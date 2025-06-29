"""
API route for managing users resources.

Provides endpoints to create Users entities.

Features:
- Standard HTTP status codes and error handling.

Endpoints:
- POST /users/     : Register a new user account.
- POST /users/login: Log in a user and return an access token.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.databases import SessionDep
from app.schemas import Feedback, TokenSchema, UserCreate
from app.services import UserService

router = APIRouter(tags=["Users"])


# POST -------------------------------------------------------------------------
@router.post(
    "/users/",
    status_code=201,
    response_model=Feedback,
    summary="creates a new User",
    description="Allows user to create an account to access the service",
)
def register_user(session: SessionDep, user_data: UserCreate):
    """
    Endpoint to create a new user.

    Args:
        session (SessionDep)  : Database session dependency.
        user_data (UserCreate): User data for registration.

    Raises:
        HTTPException: HTTP 400 Bad Request if user registration fails.
    """
    if UserService.create_user(session, user_data):
        return Feedback(detail="Successfully registered user")

    raise HTTPException(
        status_code=400,
        detail="User registration failed, email or username already exists",
    )


@router.post(
    "/users/login",
    response_model=TokenSchema,
    summary="login user",
    description="Allows an user to login and get jwt token in return",
)
def login_user(
    session: SessionDep, user_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    Endpoint to log in a user and return an access token.

    Args:
        session (SessionDep)                 : Database session dependency.
        user_data (OAuth2PasswordRequestForm): User data for login.

    Raises:
        HTTPException: HTTP 400 Bad Request if login fails.
    """
    token = UserService.login_user(session, user_data)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    return TokenSchema(access_token=token, token_type="bearer")
