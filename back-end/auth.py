#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt
from models import storage
from models.user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union
from functools import wraps
from flask import request, jsonify, abort, g


def _hash_password(password: str) -> bytes:
    """
    Hashes a password.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def _generate_uuid() -> str:
    """
    Generates a UUID.

    Returns:
        str: The generated UUID.
    """
    return str(uuid4())

def login_required(f):
    """
    Decorator that checks if the user is logged in by verifying the session ID in the cookies
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_id = request.cookies.get('session_id')
        if not session_id:
            abort(401, description="Unauthorized")

        try:
            user = storage.find_user_by(session_id=session_id)
            g.user = user # Attach the user object to flask.g
        except NoResultFound:
            abort(401, description="Unauthorized: User not logged in")
        
        return f(*args, **kwargs)
    return decorated_function

class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def register_user(self, first_name: str, last_name: str, email: str, password: str) -> User:
        """
        Registers a user.

        Args:
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The registered user.

        Raises:
            ValueError: If the user already exists.
        """
        try:
            user: User = storage.find_user_by(email=email)
        except NoResultFound:
            hashed_password: bytes = _hash_password(password)
            return storage.add_user(first_name, last_name, email, hashed_password)

        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates user credentials.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        try:
            user: User = storage.find_user_by(email=email)
        except NoResultFound:
            return False

        if bcrypt.checkpw(password.encode('utf-8'), user.password):
            return True
        return False

    def create_session(self, email: str) -> Union[str, None]:
        """
        Creates a session.

        Args:
            email (str): The email of the user.

        Returns:
            Union[str, None]: The session ID if successful, None otherwise.
        """
        try:
            user: User = storage.find_user_by(email=email)
            session_id: str = _generate_uuid()
            storage.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Gets a user from a session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            Union[User, None]: The user if found, None otherwise.
        """
        if session_id is None:
            return None

        try:
            user: User = storage.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """
        Destroys a session.

        Args:
            user_id (str): The user ID.

        Returns:
            None
        """
        if user_id is None:
            return None
        storage.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Gets a reset password token.

        Args:
            email (str): The email of the user.

        Returns:
            str: The reset password token.

        Raises:
            ValueError: If the user is not found.
        """
        try:
            user: User = storage.find_user_by(email=email)
            token: str = _generate_uuid()
            storage.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates a password.

        Args:
            reset_token (str): The reset password token.
            password (str): The new password.

        Returns:
            None

        Raises:
            ValueError: If the reset token is not found.
        """
        try:
            user: User = storage.find_user_by(reset_token=reset_token)
            hashed_password: bytes = _hash_password(password)
            storage.update_user(
                user.id,
                reset_token=None,
                password=hashed_password
            )
        except NoResultFound:
            raise ValueError
        
    def delete_user(self, email: str, password: str) -> None:
        """
        Deletes a user

        Args:
            email (str): The email of the user
            password (str): The password of the user

        Raises:
            NoResultFound: If user does not exist if the database
            ValueError: If credentials are incorrect
        """
        try:
            user: User = storage.find_user_by(email=email)
        except NoResultFound:
            raise ValueError("User not found")
        
        if not self.valid_login(email, password):
            raise ValueError("Invalid credentials")
        
        storage.delete(user)
        storage.save()
