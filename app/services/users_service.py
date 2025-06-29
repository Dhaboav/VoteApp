"""
CRUD operations for Users entities using SQLModel.

Functions:
- create_user         : Add a new User to the database.
- login_user          : Authenticate a User and return an access token.
- get_user_by_id      : Retrieve a User by id.
- get_user_by_username: Retrieve a User by username.

Handles SQLAlchemy exceptions with transaction rollback and logs errors.
"""

from datetime import timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.config import config
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
    def login_user(
        session: Session, user_data: OAuth2PasswordRequestForm
    ) -> Optional[str]:
        """
        Log in a user and return an access token.

        Args:
            session (Session): Database session for operations.
            user_data (OAuth2PasswordRequestForm): User credentials for login.

        Returns:
            Optional[str]: The access token if login is successful, otherwise None.
        """
        user = UserService.get_user_by_username(session, user_data.username)
        if not user or not AuthUtils.verify_password(user_data.password, user.password):
            return None

        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        return AuthUtils.login_token(user.id, access_token_expires)

    # UTILS -------------------------------------------------------------------------
    @staticmethod
    def get_user_by_id(session: Session, user_id: str) -> Optional[Users]:
        """
        Retrieve a user by ID from the database.

        Args:
            session (Session): Database session for operations.
            user_id (str): The ID of the user to retrieve.

        Returns:
            Optional[Users]: The Users entity if found, otherwise None.
        """
        statement = select(Users).where(Users.id == user_id)
        return session.exec(statement).first()

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
        return session.exec(statement).first()
