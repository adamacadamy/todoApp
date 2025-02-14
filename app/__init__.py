import os
from dotenv import load_dotenv

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from app.models import db
from app.models.user import User
from app.schemas import api
from app.utils.auth_utils import init_jwt
from app.routes import register_routes


""" 
env = {
    "SECRET_KEY": "asdfasdfas1233234sdafasdfas",
    "DATABASE_URI": "mysql+mysqlconnector://root:top!secret@localhost:3307/todo_db"
    "FLASK_APP": "run.py"
}
"""
load_dotenv()

login_manager = LoginManager()


def create_app() -> Flask:
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    db.init_app(app)

    init_jwt(app)

    Migrate(app, db)

    register_routes(api, app)

    api.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = "views.login"

    login_manager.user_loader(User.load_user)

    return app
