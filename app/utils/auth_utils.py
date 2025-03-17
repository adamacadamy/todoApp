import base64
from datetime import timedelta
from functools import wraps
from http import HTTPStatus
import json
import logging
from typing import Any, Optional

from flask import Flask, g, request
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    verify_jwt_in_request,
)
from flask_login import login_user

from app.models.user import User

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

basic_auth = HTTPBasicAuth()
jwt_auth = JWTManager()


def init_jwt(app: Flask) -> None:
    jwt_auth.init_app(app)


def generate_token(user: User) -> str:
    """
    data = {"access_token": f"Bearer {token}"}
    data_s = json.dumps({"access_token": f"Bearer {token}"})
           = '{\"access_token\": f\"Bearer {token}\"}'
    data =  json.loads('{\"access_token\": f\"Bearer {token}\"}')
         = {"access_token": f"Bearer {token}"}
    """
    user_data = json.dumps(
        {"username": user.username, "user_id": user.id}
    )  # '{\"username\": user.username, \"user_id\": user.id}'
    expires = timedelta(days=1)

    token = create_access_token(
        identity=user_data, expires_delta=expires
    )  #  '{\"username\": user.username, \"user_id\": user.id}'=> .ASDF3ASFDASFD3242

    return token


def verify_user_basic(username: str, password: str) -> Optional[User]:  # User | None
    logger.info(f"username: {username}, password: {password}")
    user = User.query.filter_by(username=username).first()  # user | None

    if user and User.check_password(user.password_hash, password):
        login_user(user)
        g.current_user = {
            "username": user.username,
            "user_id": user.id,
        }

        return user

    return None


def verify_user_jwt() -> Optional[User]:
    verify_jwt_in_request()  # Authorization: Bearer .ASDF3ASFDASFD3242
    user_identity = json.loads(
        get_jwt_identity()
    )  # from  .ASDF3ASFDASFD3242 =>  json.loads('{\"username\": user.username, \"user_id\": user.id}') = {"username": user.username, "user_id": user.id}
    user_id = user_identity["user_id"]
    user = User.load_user(user_id)
    if user:
        login_user(user)
        g.current_user = {
            "username": user.username,
            "user_id": user.id,
        }

        return user

    return None


def get_user_metadata(auth_header: str) -> tuple[str, str]:
    base64_credentials_meta = auth_header.split(
        " "
    )  # `Basic dXNlcjpwYXNzd29yZA==` => [ 'Basic', 'dXNlcjpwYXNzd29yZA==']
    base64_credentials = base64_credentials_meta[
        1
    ]  # base64_credentials = dXNlcjpwYXNzd29yZA==`

    credentials = base64.b64decode(base64_credentials).decode(
        "utf-8"
    )  # 'dXNlcjpwYXNzd29yZA==' => `'some username':'some hashed password'`

    provided_username, provided_password = credentials.split(
        ":"
    )  # ['some username', 'some hashed password']

    return provided_username, provided_password


def auth_required():
    def decorator(func: Any):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            """
            GET /basic-user HTTP/1.1
            Host: example.com
            HEADER:
                Authorization: `Basic dXNlcjpwYXNzd29yZA==`  or `Bearer dXNlcjpwYXNzd29yZA==`
            """
            auth_header = request.headers.get(
                "Authorization"
            )  # Basic dXNlcjpwYXNzd29yZA==  or Bearer dXNlcjpwYXNzd29yZA==

            if auth_header and auth_header.startswith("Bearer "):
                user = verify_user_jwt()  # User | None
                if not user:
                    return {"message": "Invalid credentials"}, HTTPStatus.UNAUTHORIZED

            elif auth_header and auth_header.startswith("Basic "):
                username, password = get_user_metadata(auth_header)
                user = verify_user_basic(username, password)
                if not user:
                    return {"message": "Invalid credentials"}, HTTPStatus.UNAUTHORIZED
            else:
                return {
                    "message": "Authorization header is missing or invalid"
                }, HTTPStatus.UNAUTHORIZED

            return func(*args, **kwargs)

        return wrapper

    return decorator
