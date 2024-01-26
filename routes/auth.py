from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    jwt_required,
)

from models.user import User

# initialize auth blueprint
auth = Blueprint("auth", __name__)


@auth.post("/register")
def register():
    """
    Register a new user
    """

    data: dict[str, str] = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if username is None or username.strip() == "":
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "username is required",
                }
            ),
            400,
        )  # Bad Request

    if email is None or email.strip() == "":
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "email is required",
                }
            ),
            400,
        )  # Bad Request

    if password is None or password.strip() == "":
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "password is required",
                }
            ),
            400,
        )  # Bad Request

    user = User.get_user_by_username(username)

    if user is not None:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "username already exists",
                }
            ),
            409,
        )  # Conflict

    new_user = User(username, email)

    new_user.set_password(password)
    new_user.save()

    return (
        jsonify(
            {
                "status": "success",
                "message": "User created successfully",
            }
        ),
        201,
    )  # Created


@auth.post("/login")
def login():
    """
    Login a user
    """

    data: dict[str, str] = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if username is None or username.strip() == "":
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "username is required",
                }
            ),
            400,
        )  # Bad Request

    if password is None or password.strip() == "":
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "password is required",
                }
            ),
            400,
        )  # Bad Request

    user = User.get_user_by_username(username)

    if user is None or not user.check_password(password):
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "invalid credentials",
                }
            ),
            401,
        )  # Unauthorized

    print(user.username)

    access_token = create_access_token(identity=user.username)
    refresh_token = create_refresh_token(identity=user.username)

    return (
        jsonify(
            {
                "status": "success",
                "message": "logged in successfully",
                "data": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
            },
        ),
        200,
    )  # OK


@auth.get("/whoami")
@jwt_required()
def whoami():
    """
    Get the currently logged in user
    """

    claims = get_jwt()

    return (
        jsonify(
            {
                "status": "success",
                "message": "user retrieved successfully",
                "data": {
                    "claims": claims,
                },
            }
        ),
        200,
    )  # OK
