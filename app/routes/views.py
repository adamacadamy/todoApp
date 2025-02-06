from flask import Blueprint, render_template
from app.forms.login_form import LoginForm
from app.forms.register_form import RegisterForm
from app.forms.todo_form import ToDoForm

views_bp = Blueprint("views", __name__)

@views_bp.route("/login", methods=["GET"])
def login()->str:
    form = LoginForm()
    return render_template('login.html', form=form)

@views_bp.route("/register", methods=["GET"])
def register()->str: 
    form = RegisterForm()
    return render_template('register.html', form=form)

@views_bp.route("/todo", methods=["GET"])
def todo()->str:
    form = ToDoForm()
    return render_template('todo.html', form=form)