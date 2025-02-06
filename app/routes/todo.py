from http import HTTPStatus
from flask import request
from flask_restx import Namespace, Resource
from app.models.todo import ToDo
from app.models import db
from app.schemas.todo_schema import todo_model

todo_ns = Namespace("todo", description="To-Do management")


@todo_ns.route("/")
class ToDoList(Resource):
    @todo_ns.marshal_list_with(todo_model)
    def get(self):
        """Retrieve all to-do tasks."""
        return ToDo.query.all(), HTTPStatus.OK

    @todo_ns.expect(todo_model)
    def post(self):
        """Create a new to-do task."""
        data = request.json
        new_todo = ToDo(
            task=data["task"],
            is_completed=data.get("is_completed", False),
            user_id=data["user_id"],
        )
        db.session.add(new_todo)
        db.session.commit()
        return {"message": "To-Do task created successfully."}, HTTPStatus.CREATED
