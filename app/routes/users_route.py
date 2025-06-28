"""
API route for managing users resources.

Provides endpoints to create Users entities.

Features:
- Standard HTTP status codes and error handling.

Endpoints:
- POST /users/          : Register a new user account.
- POST /users/login     : Log in a user and return an access token.
- GET /users/{username} : Retrieve a user by username.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.databases import SessionDep
from app.schemas import Feedback, TokenSchema, UserCreate, UserInfo
from app.services import UserService

router = APIRouter(tags=["Users"])


# POST -------------------------------------------------------------------------
@router.post(
    "/users/", status_code=201, response_model=Feedback, summary="creates a new User"
)
def register_user(session: SessionDep, user_data: UserCreate):
    """
    Endpoint to create a new user.

    Args:
        session (SessionDep): Database session dependency.
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


@router.post("/users/login", response_model=TokenSchema, summary="login user")
def login_user(
    session: SessionDep, user_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    Endpoint to log in a user and return an access token.

    Args:
        session (SessionDep): Database session dependency.
        user_data (OAuth2PasswordRequestForm): User data for login.

    Raises:
        HTTPException: HTTP 400 Bad Request if login fails.
    """
    token = UserService.login_user(session, user_data)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    return TokenSchema(access_token=token, token_type="bearer")


# GET -------------------------------------------------------------------------
@router.get(
    "/users/{username}", response_model=UserInfo, summary="get user by username"
)
def get_user_by_username(session: SessionDep, username: str):
    """
    Endpoint to retrieve a user by username.

    Args:
        username (str): The username of the user to retrieve.
        session (SessionDep): Database session dependency.

    Raises:
        HTTPException: HTTP 404 Not Found if user is not found.
    """
    user = UserService.get_user_by_username(session, username)
    if user:
        return UserInfo(
            email=user.email,
            username=user.username,
            created_at=user.created_at,
        )

    raise HTTPException(status_code=404, detail="User not found")
