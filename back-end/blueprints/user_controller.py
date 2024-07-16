#!/usr/bin/python3
"""
User-related endpoints for the Flask application.
"""
from flask import Blueprint, jsonify, abort, g
from auth.auth import Auth
from auth.decorators import login_required, logout_required
from utils.request_utils import get_request_data

user_bp = Blueprint('user_bp', __name__)
AUTH = Auth()

@user_bp.route('/users', methods=['POST'], strict_slashes=False)
@logout_required
def register_user() -> str:
    """
    Register a new user.
    """
    data = get_request_data(["first_name", "last_name", "email", "password"])

    try:
        AUTH.register_user(data["first_name"], data["last_name"], data["email"], data["password"])
    except ValueError:
        abort(400, description="Email already registered")

    return jsonify({"email": data["email"], "message": "user created"})

@user_bp.route('/sessions', methods=["POST"], strict_slashes=False)
@logout_required
def login() -> str:
    """
    Login user and create a session.
    """
    data = get_request_data(["email", "password"])

    if not AUTH.valid_login(data["email"], data["password"]):
        abort(403, description="Invalid Credentials")

    session_id = AUTH.create_session(data["email"])
    response = jsonify({"email": data["email"], "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response

@user_bp.route('/sessions', methods=["DELETE"], strict_slashes=False)
@login_required
def logout() -> str:
    """
    Logout user and destroy the session.
    """
    AUTH.destroy_session(g.user.id)
    response = jsonify({"email": g.user.email, "message": "logged out"})
    response.set_cookie("session_id", "", expires=0)  # Clear the session cookie

    return response

@user_bp.route('/profile', methods=['GET'], strict_slashes=False)
@login_required
def profile() -> str:
    """
    Return the profile of the logged-in user.
    """
    return jsonify({"email": g.user.email, "name": f"{g.user.first_name} {g.user.last_name}"}), 200

@user_bp.route('/reset_password', methods=["POST"], strict_slashes=False)
@login_required
def get_reset_password_token() -> str:
    """
    Get a reset password token.
    """
    data = get_request_data(["email"])

    try:
        token = AUTH.get_reset_password_token(data["email"])
        return jsonify({"email": data["email"], "reset_token": token})
    except ValueError:
        abort(403, description="Invalid Credentials")

@user_bp.route('/reset_password', methods=["PUT"], strict_slashes=False)
@login_required
def update_password() -> str:
    """
    Update the password using the reset token.
    """
    data = get_request_data(["email", "reset_token", "new_password"])

    try:
        AUTH.update_password(data["reset_token"], data["new_password"])
        return jsonify({"email": data["email"], "message": "Password updated"}), 200
    except ValueError:
        abort(403, description="Invalid credentials")

@user_bp.route('/users', methods=["DELETE"], strict_slashes=False)
@login_required
def delete_user() -> str:
    """
    Delete a user.
    """
    data = get_request_data(["email", "password"])

    try:
        AUTH.delete_user(data["email"], data["password"])
        return jsonify({"email": data["email"], "message": "User deleted"}), 200
    except ValueError as e:
        abort(403, description=e.args[0])
