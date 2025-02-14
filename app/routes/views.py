from http import HTTPStatus
from typing import Union
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import logout_user, current_user, login_required
from werkzeug.wrappers.response import Response as WerkzeugResponse

from app.forms.todo_form import ToDoForm
from app.models import db
from app.models.todo import ToDo
from app.models.user import User
from app.forms.register_form import RegisterForm
from app.forms.login_form import LoginForm
from app.utils.auth_utils import verify_user_basic


views_bp = Blueprint("views", __name__)


@views_bp.app_errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error: Exception) -> tuple[str, int]:
    return render_template("404.html"), HTTPStatus.NOT_FOUND


@views_bp.route("/home", methods=["GET"])
def home() -> str:
    """Render the homepage."""
    return render_template("home.html")


@views_bp.route("/register", methods=["GET", "POST"])
def register() -> Union[str, WerkzeugResponse]:
    regForm = RegisterForm()
    if request.method == "POST":
        requestRegForm = RegisterForm(request.form)
        if requestRegForm.validate():  # is form valid
            existing_user = User.query.filter_by(
                username=requestRegForm.username.data
            ).first()  # user | None

            if existing_user:
                # message = "Username already exists!", category="danger"
                flash(
                    "Username already exists!", "danger"
                )  # append to the flush list of notification

            else:
                new_user = User.create_user(
                    username=requestRegForm.username.data,
                    password=requestRegForm.password.data,
                    email=requestRegForm.email.data,
                )

                db.session.add(new_user)
                db.session.commit()

                flash(
                    "Registration successful! Please log in.", "success"
                )  # append to the flush list of notification
                return redirect(url_for("views.login"))
        else:
            flash("Invalid form submission. Please check your inputs.", "danger")

    return render_template("register.html", form=regForm)


@views_bp.route("/login", methods=["GET", "POST"])
def login() -> Union[str, WerkzeugResponse]:
    loginForm = LoginForm()

    if request.method == "POST":
        requestLoginForm = LoginForm(request.form)  # form submitted from the ui
        if requestLoginForm.validate():
            username = requestLoginForm.username.data
            password = requestLoginForm.password.data
            user = verify_user_basic(username, password)
            if user:
                flash("Login successful", "success")
                return redirect(url_for("views.dashboard"))

            flash("Login failure", "danger")
            return redirect(url_for("views.login"))

        else:
            flash("Invalid form submission. Please check your inputs.", "danger")

    return render_template("login.html", form=loginForm)


@views_bp.route("/logout")
def logout() -> Union[str, WerkzeugResponse]:
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("views.home"))


@views_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard() -> Union[str, WerkzeugResponse]:
    todoForm = ToDoForm()
    todos = ToDo.query.filter_by(user_id=current_user.id).all()

    if request.method == "POST":
        requestTodoForm = ToDoForm(request.form)
        if requestTodoForm.validate_on_submit():
            new_task = ToDo(
                task=requestTodoForm.task.data,
                is_completed=requestTodoForm.is_completed.data,
                user_id=current_user.id,
            )

            db.session.add(new_task)
            db.session.commit()
            flash("New task added!", "success")

            return redirect(url_for("views.dashboard"))
        else:
            flash("Invalid form submission. Please check your inputs.", "danger")

    return render_template("dashboard.html", form=todoForm, todos=todos)


@views_bp.route("/todo_edit/<int:todo_id>", methods=["GET", "POST"])
@login_required
def todo_edit(todo_id: int) -> Union[str, WerkzeugResponse]:
    todo = ToDo.query.filter_by(id=todo_id, user_id=current_user.id).first()

    if not todo:
        flash("Task not found or not authorized", "danger")
        return redirect(url_for("views.dashboard"))

    todoForm = ToDoForm(obj=todo)

    if request.method == "POST":
        requestTodoForm = ToDoForm(request.form)
        if requestTodoForm.validate_on_submit():
            todo.task = requestTodoForm.task.data
            todo.is_completed = requestTodoForm.is_completed.data

            db.session.commit()

            flash("Task updated successfully", "success")

            return redirect(url_for("views.dashboard"))

    return render_template("edit_todo.html", form=todoForm, todo=todo)


@views_bp.route("/todo_delete/<int:todo_id>", methods=["GET", "POST"])
@login_required
def todo_delete(todo_id: int) -> Union[str, WerkzeugResponse]:
    todo = ToDo.query.filter_by(id=todo_id, user_id=current_user.id).first()
    if not todo:
        flash("Task not found or not authorized", "danger")
        return redirect(url_for("views.dashboard"))

    db.session.delete(todo)
    db.session.commit()

    flash("Task deleted successfully", "success")
    return redirect(url_for("views.dashboard"))
