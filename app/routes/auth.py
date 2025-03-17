from http import HTTPStatus
from flask_login import logout_user
from flask_restx import Namespace, Resource
from flask import request

from app.schemas.user_schema import user_model, user_login_model
from app.models import db
from app.models.user import User
from app.utils.auth_utils import auth_required, generate_token, verify_user_basic

auth_ns = Namespace("auth", description="Authentication management")


@auth_ns.route("/register")
class Register(Resource):
    @auth_ns.expect(user_model)
    def post(self):
        """Register a new user"""
        data = request.json
        username, email, password = data["username"], data["email"], data["password"]
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:  # User | None
            return {
                "success": False,
                "message": "Username already exists",
            }, HTTPStatus.CONFLICT

        new_user = User.create_user(username, email, password)

        db.session.add(new_user)
        db.session.commit()

        return {
            "success": True,
            "message": "User registered successfully",
        }, HTTPStatus.CREATED


@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(user_login_model)
    def post(self):
        """Authenticate user"""
        data = request.json
        username = data.get("username")
        password = data.get("password")

        user = verify_user_basic(username, password)
        if not user:
            return {"message": "Invalid username or password"}, HTTPStatus.UNAUTHORIZED

        token = generate_token(user)
        return {
            "success": True,
            "message": "Logged in successfully",
            "token": f"Bearer {token}",
        }, HTTPStatus.OK


@auth_ns.route("/logout")
class Logout(Resource):
    @auth_ns.doc(security=["basic", "jwt"])
    @auth_required()
    def get(self):
        """Logout user"""
        logout_user()
        return {"success": True, "message": "Logged out successfully"}, HTTPStatus.OK
