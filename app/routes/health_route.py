"""
Health check API route.

Defines a simple endpoint to verify that the service is up and running.
Returns a JSON response with a "status" key set to "ok".
"""

from fastapi import APIRouter

from app.schemas import Feedback

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=Feedback)
def health_check():
    """
    Simple health check endpoint.
    Returns a JSON response with a detail "OK".
    """
    return Feedback(detail="OK")
