from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

from lib.extensions import db, jwt
from models.user import TokenBlocklist
from routes import auth, book, user

# -----------------------------------------------------------------------------------------------
# Initialize Flask App
# -----------------------------------------------------------------------------------------------

app = Flask(__name__)


# -----------------------------------------------------------------------------------------------
# Load Config from Environment
# -----------------------------------------------------------------------------------------------

app.config.from_prefixed_env()

# -----------------------------------------------------------------------------------------------
# Initialize Extensions
# -----------------------------------------------------------------------------------------------

db.init_app(app)
jwt.init_app(app)

# -----------------------------------------------------------------------------------------------
# Swagger Documentation
# -----------------------------------------------------------------------------------------------


SWAGGER_URL = "/api/docs"
DOCS_API_URL = "/static/swagger.json"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    DOCS_API_URL,
    config={"app_name": "Vidyapeeth Bookstore"},
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #     "clientId": "your-client-id",
    #     "clientSecret": "your-client-secret-if-required",
    #     "realm": "your-realms",
    #     "appName": "your-app-name",
    #     "scopeSeparator": " ",
    #     "additionalQueryStringParams": {"test": "hello"},
    # },
)


# -----------------------------------------------------------------------------------------------
# Register Blueprints
# -----------------------------------------------------------------------------------------------


app.register_blueprint(swaggerui_blueprint)

app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(book, url_prefix="/book")


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


@jwt.token_in_blocklist_loader
def token_in_blocklist_callback(jwt_headers, jwt_data):
    jti = jwt_data["jti"]

    token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()

    return token is not None
