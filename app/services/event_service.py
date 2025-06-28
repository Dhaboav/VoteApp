"""
CRUD operations for Event entities using SQLModel.

Functions:
- create_event: Add a new Event to the database.

Handles SQLAlchemy exceptions with transaction rollback and logs errors.
"""

from uuid import UUID

from sqlmodel import Session

from app.models import Choice, Event
from app.schemas import EventCreate


class EventService:

    @staticmethod
    def create_event(session: Session, user_id: UUID, event_data: EventCreate) -> bool:
        """
        Create a new event in the database.

        Args:
            session (Session)       : Database session for operations.
            user_id (UUID)          : ID of the user creating the event.
            event_data (EventCreate): Input event data.

        Returns:
            bool: True if event was created successfully, False if choices is not between 2 and 4.
        """

        if not 2 <= len(event_data.choices) <= 4:
            return False

        db_obj = Event(
            title=event_data.name, desc=event_data.description, creator_id=user_id
        )

        try:
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)

            # Add each choice
            for choice in event_data.choices:
                db_choice = Choice(choice=choice.choice, event_id=db_obj.id)
                session.add(db_choice)

            session.commit()
            return True

        except Exception:
            session.rollback()
            return False
