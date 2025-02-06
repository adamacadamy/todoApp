from http import HTTPStatus
from flask import request
from flask_restx import Namespace, Resource
from app.models.user import User
from app.models import db
from app.schemas.user_schema import user_model

auth_ns = Namespace("auth", description="Authentication management")

@auth_ns.route("/register")
class Register(Resource):
    @auth_ns.expect(user_model)
    def post(self):
        data = request.json
        username, email, password = data["username"], data["email"], data["password"]

        if User.query.filter_by(username=username).first():
            return {"message": "Username already exists"}, HTTPStatus.CONFLICT
        if User.query.filter_by(email=email).first():
            return {"message": "Email already exists"}, HTTPStatus.CONFLICT

        new_user = User.create_user(username, email, password)
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully"}, HTTPStatus.CREATED
