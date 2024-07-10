#!/usr/bin/python3
"""

"""
from flask import request, Blueprint, jsonify, abort, redirect, g
from auth import Auth, login_required

user_bp = Blueprint('user_bp', __name__)
AUTH = Auth()

@user_bp.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """
    Register user
    """
    first_name = request.form.get("first_name")
    if not first_name:
        abort(400, description="Missing first name")

    last_name = request.form.get("last_name")
    if not last_name:
        abort(400, description="Missing last name")

    email = request.form.get("email")
    if not email:
        abort(400, description="Missing email")

    password = request.form.get("password")
    if not password:
        abort(400, description="Missing password")

    try:
        AUTH.register_user(first_name, last_name, email, password)
    except ValueError:
        abort(400, description="Email already registered")
    return jsonify({"email": email, "message": "user created"})


@user_bp.route('/sessions', methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    Login method
    """
    email = request.form.get("email")
    if not email:
        abort(403, description="Missing email")

    password = request.form.get("password")
    if not password:
        abort(403, description="Missing password")

    if not AUTH.valid_login(email, password):
        abort(403, desciption="Invalid Credentials")

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response

@user_bp.route('/sessions', methods=["DELETE"], strict_slashes=False)
@login_required
def logout() -> str:
    """
    Logout method
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403, description="Missing session id")

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(404, description="User not found")

    AUTH.destroy_session(user.id)

    return redirect('/')

@user_bp.route('/profile', methods=['GET'], strict_slashes=False)
@login_required
def profile() -> str:
    """
    Returns the profile of the session id
    """
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if user is None:
        abort(404, description="User not found")

    return jsonify({"email": user.email, "name": f"{user.first_name} {user.last_name}"}), 200


@user_bp.route('/reset_password', methods=["POST"], strict_slashes=False)
@login_required
def get_reset_password_token() -> str:
    """
    Get reset password token
    """
    email = request.form.get('email')
    if not email:
        abort(400, description="Missing email")

    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token})
    except ValueError:
        abort(403, desciption="Invalid Credentials")


@user_bp.route('/reset_password', methods=["PUT"], strict_slashes=False)
@login_required
def update_password() -> str:
    """
    Update password
    """
    email = request.form.get('email')
    if not email:
        abort(400, description="Missing email")

    reset_token = request.form.get('reset_token')
    if not reset_token:
        abort(400, description="Missing reset token")

    new_password = request.form.get('new_password')
    if not new_password:
        abort(400, description="Missing new password")

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403, description="Invalid credentials")

@user_bp.route('/users', methods=["DELETE"], strict_slashes=False)
@login_required
def delete_user() -> str:
    """
    Deletes a user
    """
    email = request.form.get("email")
    if not email:
        abort(400, description="Missing Email")

    password = request.form.get("password")
    if not password:
        abort(400, description="Missing password")

    try:
        AUTH.delete_user(email, password)
        return jsonify({"email": email, "message": "User deleted"})
    except ValueError as e:
        abort(403, description=e.args[0])
