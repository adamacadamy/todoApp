from app.models import db


class ToDo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "task": self.task,
            "is_completed": self.is_completed,
            "user_id": self.user_id,
        }

    @staticmethod
    def to_list_dict(todos: list["ToDo"]) -> list[dict]:
        return [todo.to_dict() for todo in todos]
