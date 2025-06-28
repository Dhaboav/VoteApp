"""
API routes for managing event resources.

Provides endpoints for creating event entities.

Features:
- Standard HTTP status codes and error handling.

Endpoints:
- POST /events: Create a new event.
"""

from fastapi import APIRouter, HTTPException

from app.databases import SessionDep
from app.schemas import EventCreate, Feedback
from app.services import EventService

from .deps import CurrentUserDep

router = APIRouter(tags=["Events"])


@router.post(
    "/events/", status_code=201, response_model=Feedback, summary="creates a new Event"
)
def create_event(session: SessionDep, user: CurrentUserDep, event_data: EventCreate):
    """
    Endpoint to create a new voting event.

    Args:
        session (SessionDep)    : Database session dependency.
        user (CurrentDep)       : The currently authenticated user from the JWT token.
        event_data (EventCreate): Data for the event to be created.

    Raises:
        HTTPException: 400 Bad Request if event creation fails.
    """

    if EventService.create_event(session, user.id, event_data):
        return Feedback(detail="Successfully create event")

    raise HTTPException(
        status_code=400,
        detail="Failed to create event, choices must be between 2 and 4!",
    )
