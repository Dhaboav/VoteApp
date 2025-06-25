"""
API route for managing users resources.

Provides endpoints to create Users entities.

Features:
- Standard HTTP status codes and error handling.

Endpoints:
- POST /users/: Register a new user account.
"""

from fastapi import APIRouter, HTTPException

from app.databases import SessionDep
from app.schemas import Feedback, UserCreate
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
