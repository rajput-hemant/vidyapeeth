from flask import jsonify
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

# -----------------------------------------------------------------------------------------------
# DB Extensions
# -----------------------------------------------------------------------------------------------

db = SQLAlchemy()


# -----------------------------------------------------------------------------------------------
# JWT Extensions
# -----------------------------------------------------------------------------------------------

jwt = JWTManager()

# -----------------------------------------------------------------------------------------------
# Additional Claims
# -----------------------------------------------------------------------------------------------


# @jwt.additional_claims_loader
# def make_additional_claims(identity):
#     """
#     Add additional claims to the JWT
#     """

#     # TODO: Add additional claims here

#     return (
#         jsonify(
#             {
#                 "status": "pending",
#                 "message": "This route is not yet implemented",
#             }
#         ),
#         200,
#     )


# -----------------------------------------------------------------------------------------------
# JWT Error Handlers/Callbacks
# -----------------------------------------------------------------------------------------------


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """
    Callback function for when an expired token is used
    """
    return (
        jsonify(
            {
                "status": "failed",
                "error": "token_expired",
                "message": "The token has expired",
            }
        ),
        401,
    )  # Unauthorized


@jwt.invalid_token_loader
def invalid_token_callback(error):
    """
    Callback function for when an invalid token is used
    """
    return (
        jsonify(
            {
                "status": "failed",
                "error": "invalid_token",
                "message": "Signature verification failed",
            }
        ),
        401,
    )  # Unauthorized


@jwt.unauthorized_loader
def unauthorized_callback(error):
    """
    Callback function for when a token is missing
    """
    return (
        jsonify(
            {
                "status": "failed",
                "error": "authorization_required",
                "message": "Request does not contain an access token",
            }
        ),
        401,
    )  # Unauthorized
