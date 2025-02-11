#!/usr/bin/python3
"""

"""
from functools import wraps
from flask import request, abort, g
from models import storage
from sqlalchemy.orm.exc import NoResultFound
from utils.request_utils import get_request_data


def login_required(f):
    """
    Decorator that checks if the user is logged in by verifying the session ID in the request.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_id = get_request_data(["session_id"]).get("session_id")
        if not session_id:
            abort(401, description="Unauthorized")

        try:
            user = storage.find_user_by(session_id=session_id)
            g.user = user # Attach the user object to flask.g
        except NoResultFound:
            abort(401, description="Unauthorized: User not logged in")
        
        return f(*args, **kwargs)
    return decorated_function

def logout_required(f):
    """
    Decorator that ensures the user is logged out before proceeding
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_id = request.json.get("session_id")
        if session_id:
            try:
                user = storage.find_user_by(session_id=session_id)
                if user:
                    abort(401, description="Unauthorized: User already logged in")
            except NoResultFound:
                pass  # If no user found, continue as normal

        return f(*args, **kwargs)
    return decorated_function
