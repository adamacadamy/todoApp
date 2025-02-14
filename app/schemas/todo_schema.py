from flask_restx import fields

from app.schemas import api

todo_model = api.model(
    "ToDo",
    {
        "id": fields.Integer(readonly=True, description="To-Do ID"),
        "task": fields.String(required=True, description="Task description"),
        "is_completed": fields.Boolean(description="Completion status"),
    },
)


todo_update_model = api.model(
    "ToDoUpdate",
    {
        "task": fields.String(required=True, description="Task description"),
        "is_completed": fields.Boolean(description="Completion status"),
    },
)
