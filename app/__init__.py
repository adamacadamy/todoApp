import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from dotenv import load_dotenv

from app.routes import register_routes
from app.schemas import api
from app.models import db

# Load environmental variables
# os.env = {
#    "SECRET_KEY": "your_secret_key"
#    "DATABASE_URI": "mysql+mysqlconnector://root:top!secreat@localhost:3307/todo_db"
#    "FLASK_APP": "run.py"
# }

load_dotenv()

def create_app() -> Flask:
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    
    db.init_app(app)
    
    Migrate(app, db)
    
    api.init_app(app)
    
    register_routes(api, app)
    
    return app