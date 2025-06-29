"""
CRUD operations for Event and Vote entities using SQLModel.

Functions:
- create_event  : Add a new Event to the database.
- create_vote   : Add a new Vote to the database.
- verify_choice : Utility function to verify choice.
- is_vote       : Utility function to verify is user already vote or not.

Handles SQLAlchemy exceptions with transaction rollback and logs errors.
"""

from datetime import datetime
from typing import Optional, Tuple
from uuid import UUID

from sqlmodel import Session, select

from app.models import Choice, Event, Vote
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
            title=event_data.name,
            desc=event_data.description,
            creator_id=user_id,
            expires_at=event_data.expires_at,
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

    @staticmethod
    def create_vote(
        session: Session, user_id: UUID, event_id: UUID, choice: str
    ) -> Tuple[bool, str]:
        """
        votes an event and save it in the database.

        Args:
            session (Session)  : Database session for operations.
            user_id (UUID)     : ID of the user votes the event.
            event_id (UUID)    : ID of the event .
            choice (str)       : ID of the choice.

        Returns:
            Tuple[bool, str]:
                - `True` and a success message if the vote is successfully cast.
                - `False` and an error message if any validation fails or an exception occurs.
        """
        is_event = session.get(Event, event_id)

        if not is_event:
            return False, "Event not found."

        elif is_event.expires_at and datetime.now() > is_event.expires_at:
            return False, "Voting for this event has ended."

        choice_check = EventService.verify_choice(session, choice, event_id)
        if not choice_check:
            return False, "The selected choice does not exist for this event."

        if EventService.is_vote(session, user_id, event_id):
            return False, "You have already voted in this event."

        db_obj = Vote(user_id=user_id, event_id=event_id, choice_id=choice_check.id)
        try:
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)

            return True, "Successfully votes event"

        except Exception:
            session.rollback()
            return False, "Something wrong."

    # UTILS -------------------------------------------------------------------------
    @staticmethod
    def verify_choice(
        session: Session, event_id: UUID, choice: str
    ) -> Optional[Choice]:
        """
        Verify a choice by event id from the database.

        Args:
            session (Session)  : Database session for operations.
            event_id (UUID)    : ID of the event.
            choice (str)       : The choice user choose.

        Returns:
            Optional[Choice]: The Choice entity if found, otherwise None.
        """

        statment = select(Choice).where(
            Choice.event_id == event_id, Choice.choice == choice
        )

        return session.exec(statment).first()

    @staticmethod
    def is_vote(session: Session, user_id: UUID, event_id: UUID) -> Optional[Vote]:
        """
        Verify is a user already vote or not.

        Args:
            session (Session) : Database session for operations.
            user_id (UUID)    : ID of the user votes the event.
            event_id (str)    : ID of the event.

        Returns:
            Optional[Vote]: The Vote entity if found, otherwise None.
        """
        statment = select(Vote).where(
            Vote.user_id == user_id, Vote.event_id == event_id
        )
        return session.exec(statment).first()
