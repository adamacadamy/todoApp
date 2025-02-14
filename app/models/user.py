# built in libraries
# import os, import json, import dotenv ....

# pip installed libraries
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# local packages
from app.models import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(225), nullable=False)
    # Other relevant fields...
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    todos = db.relationship("ToDo", backref="user", lazy=True)

    @staticmethod
    def check_password(password_hash, password: str) -> bool:
        """Verify a user's password using hashing"""
        return check_password_hash(password_hash, password)

    @staticmethod
    def create_user(username: str, email: str, password: str) -> "User":
        """Create a new user with a hashed password"""
        # password=adam131231, generate_password_hash(password) => rasfdpasfydkhjsdfa123423 asdfha
        hashed_password = generate_password_hash(password)
        return User(
            username=username,
            email=email,
            password_hash=hashed_password,
            is_active=True,
        )

    @staticmethod
    def load_user(user_id: int) -> "User":
        """Load a user for Flask-Login session management"""
        return User.query.get(int(user_id))
