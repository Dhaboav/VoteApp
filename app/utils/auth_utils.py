"""
Utility functions for password hashing and verification.

Functions:
- encrypted_password: Hashes a plain text password.
- verify_password   : Verifies a plain text password against a hashed password.
- login_token       : Generates a JWT token for user login with an expiration time.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Union

import jwt
from passlib.context import CryptContext

from app.config import config


class AuthUtils:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def encrypted_password(password: str) -> str:
        """
        Hashes a plain text password using bcrypt.

        Args:
            password (str): The plain text password to hash.

        Returns:
            str: The hashed password.
        """
        return AuthUtils.pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a plain text password against a hashed password.

        Args:
            plain_password (str) : The plain text password to verify.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the plain password matches the hashed password, False otherwise.
        """
        return AuthUtils.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def login_token(subject: Union[str, Any], expires_delta: timedelta) -> str:
        """
        Generates a JWT token for user login with an expiration time.

        Args:
            subject (Union[str, Any]): The subject for which the token is generated (e.g., user ID).
            expires_delta (timedelta): The duration after which the token will expire.

        Returns:
            str: The encoded JWT token.
        """

        expire = datetime.now(timezone.utc) + expires_delta
        to_encode = {"exp": expire, "sub": str(subject)}
        encode_jwt = jwt.encode(
            to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM
        )
        return encode_jwt
