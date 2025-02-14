from flask_restx import fields
from app.schemas import api

user_model = api.model(
    "User",
    {
        "id": fields.Integer(readonly=True, description="User ID"),
        "username": fields.String(required=True, description="Username"),
        "email": fields.String(required=True, description="Email"),
        "password": fields.String(required=True, description="Password"),
    },
)

user_login_model = api.model(
    "UserLogin",
    {
        "username": fields.String(required=True, description="Username"),
        "password": fields.String(required=True, description="Password"),
    },
)
