from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from lib.schemas import UserSchema
from models.user import User

user = Blueprint("user", __name__)


@user.get("/all")
@jwt_required()
def get_all_users():
    """
    Get all users
    TODO: Restrict this route to admin users only
    """

    query_params = request.args

    page = query_params.get("page", 1, type=int)
    per_page = query_params.get("per_page", 10, type=int)

    users = User.query.paginate(page=page, per_page=per_page)

    result = UserSchema().dump(users, many=True)

    return (
        jsonify(
            {
                "status": "success",
                "message": "users retrieved successfully",
                "data": result,
            }
        ),
        200,
    )  # OK
