from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class ToDoForm(FlaskForm):
    task = StringField("Task", validators=[DataRequired()])
    is_completed = BooleanField("Completed")
    submit = SubmitField("Add Task")
