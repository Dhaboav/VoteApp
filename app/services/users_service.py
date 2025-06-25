"""
CRUD operations for Users entities using SQLModel.

Functions:
- create_user           : Add a new User to the database.
- get_all_users         : Retrieve all Users from the database.
- get_user_by_username  : Retrieve a User by username.

Handles SQLAlchemy exceptions with transaction rollback and logs errors.
"""

from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.models import Users
from app.schemas import UserCreate
from app.utils import AuthUtils


class UserService:

    @staticmethod
    def create_user(session: Session, user: UserCreate) -> bool:
        """
        Create a new user in the database.

        Args:
            session (Session): Database session for operations.
            user (UserCreate): User data to be created.

        Returns:
            bool: True if user was created successfully, False if email or username already exists.
        """

        db_obj = Users.model_validate(
            user,
            update={"password": AuthUtils.encrypted_password(user.password)},
        )

        try:
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return True

        except IntegrityError:
            session.rollback()
            return False

    @staticmethod
    def get_all_users(session: Session) -> List[Users]:
        """
        Retrieve all users from the database.

        Args:
            session (Session): Database session for operations.

        Returns:
            List[Users]: List of all Users entities.
        """
        statement = select(Users)
        return session.exec(statement).all()

    @staticmethod
    def get_user_by_username(session: Session, username: str) -> Optional[Users]:
        """
        Retrieve a user by username from the database.

        Args:
            session (Session): Database session for operations.
            username (str): The username of the user to retrieve.

        Returns:
            Optional[Users]: The Users entity if found, otherwise None.
        """
        statement = select(Users).where(Users.username == username)
        result = session.exec(statement).first()
        return result if result else None
