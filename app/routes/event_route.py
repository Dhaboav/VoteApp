"""
API routes for managing event resources.

Provides endpoints for creating event entities.

Features:
- Standard HTTP status codes and error handling.

Endpoints:
- POST /events                  : Create a new event.
- POST /vote/{event_id}/{choice}: Create a new vote on event.
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.databases import SessionDep
from app.schemas import EventCreate, Feedback
from app.services import EventService

from .deps import CurrentUserDep

router = APIRouter(tags=["Events"])


# POST -------------------------------------------------------------------------
@router.post(
    "/events/",
    status_code=201,
    response_model=Feedback,
    summary="creates a new Event",
    description="Allows an authenticated user to create vote with 2-4 choices",
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


@router.post(
    "/vote/{event_id}/{choice}",
    response_model=Feedback,
    summary="vote on an Event",
    description="Allows an authenticated user to vote on a specific choice for a given event.",
)
def user_votes(session: SessionDep, user: CurrentUserDep, event_id: str, choice: str):
    """
    Endpoint to votes the event.

    Args:
        session (SessionDep): Database session dependency.
        user (CurrentDep)   : The currently authenticated user from the JWT token.
        events (str)        : UUID of the event (as a string path parameter).
        choice (str)        : The choice text selected by the user.

    Raises HTTPException:
        - 422: If the event ID is not a valid UUID.
        - 404: If the event or choice is not found.
        - 403: If the event's voting period has expired.
        - 409: If the user has already voted in the event.
        - 400: For other unexpected errors.
    """

    try:
        event_id = UUID(event_id)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid event UUID")

    success, message = EventService.create_vote(session, user.id, event_id, choice)

    if success:
        return Feedback(detail=message)

    error_status_map = {
        "Event not found.": 404,
        "The selected choice does not exist for this event.": 404,
        "Voting for this event has ended.": 403,
        "You have already voted in this event.": 409,
    }

    status_code = error_status_map.get(message, 400)
    raise HTTPException(status_code=status_code, detail=message)
