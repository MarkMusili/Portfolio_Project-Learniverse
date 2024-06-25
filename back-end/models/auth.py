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


def _hash_password(password: str) -> bytes:
    """
    Hashes a password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generate uuid
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database
    """
    def register_user(self,
                 first_name: str,
                 last_name: str,
                 email: str,
                 password: str) -> User:
        """
        Registers a user
        """
        try:
            storage.find_user_by(email=email)
        except NoResultFound:
            return storage.add_user(first_name, last_name, email, _hash_password(password))

        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validation of credentials
        """
        try:
            user = storage.find_user_by(email=email)
        except NoResultFound:
            return False

        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return True
        return False

    def create_session(self, email: str) -> str:
        """
        Creates a session
        """
        try:
            user = storage.find_user_by(email=email)
            session_id = _generate_uuid()
            storage.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Get user from session id
        """
        if session_id is None:
            return None

        try:
            user = storage.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """
        Destroys a session
        """
        if user_id is None:
            return None
        storage.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Gets reset_password token
        """
        try:
            user = storage.find_user_by(email=email)
            token = _generate_uuid()
            storage.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates a password
        """
        try:
            user = storage.find_user_by(reset_token=reset_token)
            storage.update_user(
                user.id,
                reset_token=None,
                password=_hash_password(password)
                )
        except NoResultFound:
            raise ValueError
