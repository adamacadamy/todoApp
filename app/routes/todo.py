from http import HTTPStatus
from flask import g, request
from flask_restx import Namespace, Resource

from app.models import db
from app.models.todo import ToDo
from app.utils.auth_utils import auth_required
from app.schemas.todo_schema import todo_model, todo_update_model


todo_ns = Namespace("task", description="To-Do management")


@todo_ns.route("/")
class ToDoList(Resource):
    @todo_ns.doc(security=["basic", "jwt"])
    @auth_required()
    def get(self) -> tuple[dict, int]:
        """Retrieve all to-do tasks."""
        todos = ToDo.query.filter_by(
            user_id=g.current_user["user_id"],
        ).all()
        return ToDo.to_list_dict(todos), HTTPStatus.OK

    @todo_ns.doc(security=["basic", "jwt"])
    @auth_required()
    @todo_ns.expect(todo_model)
    def post(self) -> tuple[dict, int]:
        """Create a new to-do task."""
        data = request.json
        if data:
            task = data.get("task", "")
            is_completed = data.get("is_completed", False)
            new_todo = ToDo(
                task=task,
                is_completed=is_completed,
                user_id=g.current_user["user_id"],
            )
            db.session.add(new_todo)
            db.session.commit()
            return {"message": "To-Do task created successfully."}, HTTPStatus.CREATED

        return {
            "message": "To-Do task not created, payload is corrupt."
        }, HTTPStatus.BAD_REQUEST


@todo_ns.route("/<int:task_id>")
class ToDoResource(Resource):
    @todo_ns.doc(security=["basic", "jwt"])
    @auth_required()
    @todo_ns.marshal_with(todo_model)
    def get(self, task_id) -> tuple[dict, int]:
        """Retrieve a specific to-do task."""
        todo = ToDo.query.get_or_404(task_id)
        user_id = g.current_user["user_id"]
        if todo.user_id != user_id:
            return {
                "message": "no task identified by the provided task user id exists"
            }, HTTPStatus.NOT_FOUND

        return todo, HTTPStatus.OK

    @todo_ns.doc(security=["basic", "jwt"])
    @auth_required()
    @todo_ns.expect(todo_update_model)
    def put(self, task_id) -> tuple[dict, int]:
        """Update a specific to-do task."""
        data = request.json
        if not data:
            return {
                "message": "To-Do task not created, payload is corrupt."
            }, HTTPStatus.BAD_REQUEST

        todo = ToDo.query.get_or_404(task_id)
        user_id = g.current_user["user_id"]

        if not todo or todo.user_id != user_id:
            return {
                "message": "no task identified by the provided task user id exists"
            }, HTTPStatus.NOT_FOUND

        todo.task = data["task"]
        todo.is_completed = data.get("is_completed", todo.is_completed)
        todo.user_id = g.current_user["user_id"]
        db.session.commit()

        return {"message": "To-Do task updated successfully."}, HTTPStatus.OK

    @todo_ns.doc(security=["basic", "jwt"])
    @auth_required()
    def delete(self, task_id) -> tuple[dict, int]:
        """Delete a specific to-do task."""
        todo = ToDo.query.get_or_404(task_id)
        user_id = g.current_user["user_id"]

        if todo.user_id != user_id:
            return {
                "message": "no task identified by the provided task user id exists"
            }, HTTPStatus.NOT_FOUND

        db.session.delete(todo)
        db.session.commit()
        return {"message": "To-Do task deleted successfully."}, HTTPStatus.NO_CONTENT
