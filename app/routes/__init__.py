from flask_restx import Api
from flask import Flask

from app.routes.auth import auth_ns
from app.routes.todo import todo_ns
from app.routes.views import views_bp


def register_routes(api: Api, app: Flask) -> None:
    # register api's
    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(todo_ns, path="/task")

    # register views
    app.register_blueprint(views_bp)
