"""
CRUD operations for Users entities using SQLModel.

Functions:
- create_user: Add a new User to the database.

Handles SQLAlchemy exceptions with transaction rollback and logs errors.
"""

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

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
