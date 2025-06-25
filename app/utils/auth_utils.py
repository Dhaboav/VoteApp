"""
Utility functions for password hashing and verification.

Functions:
- encrypted_password: Hashes a plain text password.
- verify_password: Verifies a plain text password against a hashed password.
"""

from passlib.context import CryptContext


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
            plain_password (str): The plain text password to verify.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the plain password matches the hashed password, False otherwise.
        """
        return AuthUtils.pwd_context.verify(plain_password, hashed_password)
