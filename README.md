# TODO APP

A simple task management application that allows users to create, manage, and track tasks efficiently. This app provides authentication, task organization, and a user-friendly interface for seamless task handling.

## Specification

## 1. Data Model

## 1.1 User Model

- `id` (Primary Key)
- `username` (String, Unique)
- `password` (String, Hashed)
- `email` (String, Unique)
- Other relevant fields...

## 1.2 ToDo Model

- `id` (Primary Key)
- `task` (String)
- `is_complete` (Boolean, Default: False)
- `user_id` (Foreign Key to User)
- Other relevant fields...

## 2. Activities [BL(Business Logic)]

## 2.1 User Management

- Register
- Login (Authentication)
- Logout

## 2.2 Task Management

- Create a Task
- Read/View Tasks
- Update a Task
- Delete a Task

## 3. REST API

## 3.1 User Management Endpoints

- **POST** `/register` - Register a new user  
- **POST** `/login` - Authenticate user
- **GET** `/logout` - Logout user

## 3.2 Task Management Endpoints

- **POST** `/tasks` - Create a new task
- **GET** `/tasks` - Retrieve all tasks for the logged-in user
- **GET** `/tasks/{task_id}` - Retrieve a specific task
- **PUT** `/tasks/{task_id}` - Update a task
- **DELETE** `/tasks/{task_id}` - Delete a task

## 3.3 Schemas

#### 3.3.1 User Schema

- `id` (Integer, ReadOnly)
- `username` (String, Required)
- `email` (String, Required, Unique)
- `password` (String, Required)

#### 3.3.2 User login Schema

- `username` (String, Required)
- `password` (String, Required)

#### 3.3.3 Task Schema

- `id` (Integer, ReadOnly)
- `task` (String, Required)
- `is_complete` (Boolean, Default: False)

#### 3.3.4 Task Update Schema

- `task` (String, Required)
- `is_complete` (Boolean, Default: False)

---

## 4. UI Pages

### 4.1 Registration Page

- **Features**  
  - register new user

- **Form Fields**
  - Username (Input Text)
  - Email (Input Text)
  - Password (Input Password)
  - Submit Button

### 4.2 Login Page

- **Features**
  - authenticate user

- **Form Fields**
  - Username (Input Text)
  - Password (Input Password)
  - Submit Button

### 4.3 Dashboard

- **Features**
  - Task Creation (Add new tasks)  Operations
  - Task Get/list  Operations
  - Task Update/Edit Operations
  - Task Delete/Remove Operations

### 4.3.1 Dashboard Task Edit page

- **Features**
  - update selected task

- **Form Fields**
  - Task (Input Text)
  - Is Completed (Checkbox)
  - Submit Button

### 4.4 404 page

- **Features**
  - display meaningful information for page or content not found

## 4.4 Forms

#### 4.4.1 Login Form

- Username (Input Text)
- Password (Input Password)
- Submit Button

#### 4.4.2 Registration Form

- Username (Input Text)
- Email (Input Text)
- Password (Input Password)
- Submit Button

#### 4.4.3 Task Form

- Task (Input Text)
- Is Completed (Checkbox)
- Submit Button

## 5. Views

### 5.1 Error Handling

- **404 Page Not Found** - Render `404.html` template

### 5.2 Authentication

- **Login Page (`/login`)**
  - GET: Render login form in the `login.html`
  - POST: Authenticate user and redirect to `dashboard page`

- **Register Page (`/register`)**
  - GET: Render registration form  in the `register.html`
  - POST: Register new user and redirect to `login page`

- **Logout (`/logout`)**
  - Logs out user and redirects to `home page`

## 5.3 Home  

- **Landing Page(`/home`)** - Render `home.html` template

## 5.4 Dashboard

- **Dashboard page (`/dashboard`)**
  - GET: Render user's tasks list and display in the `dashboard.html` [edit/delete tasks included in the list]
  - GET: Render tasks form and display in the `dashboard.html`
  - POST: Add a new task

### 5.5 Task Management

- **Task Edit (`/todo/<int:todo_id>`)**
  - GET: Render task edit form  in the `edit_todo.html`
  - POST: Update or delete task

## 6. Scaffold Structure

```text
todo-app/
├── .gitignore               # Ignore unnecessary files
├── .env                     # Environment variables
├── .vscode/                 # VSCode settings
│   ├── settings.json        # Workspace settings
│   └── launch.json          # Debugging configurations
├── app/                     # Application logic
│   ├── __init__.py          # Initialize Flask app
│   ├── utils/               # Database models
│   │   ├── __init__.py      # package file
│   │   ├── auth_utils.py    # User authentication utilities
│   ├── models/              # Database models
│   │   ├── __init__.py      # Initialize models
│   │   ├── user.py          # User model
│   │   └── todo.py          # ToDo model
│   ├── routes/              # Application routes
│   │   ├── __init__.py      # Initialize routes
│   │   ├── auth.py          # Authentication routes
│   │   ├── todo.py          # ToDo routes
│   │   └── views.py         # View routes
│   ├── schemas/             # API schemas
│   │   ├── __init__.py      # Initialize schemas
│   │   ├── user_schema.py   # User schema
│   │   └── todo_schema.py   # ToDo schema
│   ├── forms/               # Web forms
│   │   ├── __init__.py      # Initialize forms
│   │   ├── login_form.py    # Login form
│   │   ├── register_form.py # Registration form
│   │   └── todo_form.py     # ToDo form
│   ├── templates/           # HTML templates
│   │   ├── base.html        # Base template
│   │   ├── login.html       # Login template
|   |   ├── home.html        # Home page
|   |   ├── dashboard.html   # Dashboard page
|   |   ├── edit_todo.html   # Edit ToDo page
│   │   ├── register.html    # Register template
│   │   ├── todo.html        # ToDo template
│   │   └── 404.html         # 404 error template
│   └── static/              # Static files
│       ├── style.css        # Stylesheet
│       └── script.js        # JavaScript file
├── migrations/              # Flask-Migrate folder
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md                # Project documentation
```

## 7. Scaffold Script

The following script automates the creation of the Flask project structure, including virtual environment setup, installing dependencies, and populating config files.

```python
from pathlib import Path
import subprocess
import json

def create_flask_scaffold(parent: Path, structure: dict):
    stack = [(parent, structure)]
    while stack:
        current_parent, current_structure = stack.pop()
        for name, content in current_structure.items():
            path = current_parent / name
            if isinstance(content, dict):
                path.mkdir(parents=True, exist_ok=True)
                stack.append((path, content))
            else:
                path.touch(exist_ok=True)
                if content:
                    path.write_text(content)

def setup_virtualenv(parent: Path):
    venv_path = parent / ".venv"
    subprocess.run(["python3", "-m", "venv", str(venv_path)])
    subprocess.run([str(venv_path / "bin/pip"), "install", "-r", str(parent / "requirements.txt")])

project_structure = {
    ".gitignore": "",
    ".env": "",
    ".vscode": {
        "settings.json": json.dumps({
            "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
            "editor.formatOnSave": True
        }, indent=4),
        "launch.json": json.dumps({
            "version": "0.2.0",
            "configurations": [
                {
                    "name": "Python: Run run.py",
                    "type": "python",
                    "request": "launch",
                    "program": "${workspaceFolder}/run.py",
                    "console": "integratedTerminal",
                    "envFile": "${workspaceFolder}/.env",
                    "pythonPath": "${workspaceFolder}/.venv/bin/python"
                }
            ]
        }, indent=4)
    },
    "README.md": "",
    "requirements.txt": """alembic==1.14.0
aniso8601==9.0.1
attrs==24.3.0
blinker==1.9.0
click==8.1.7
Flask==2.2.5
Flask-HTTPAuth==4.8.0
Flask-JWT-Extended==4.4.4
Flask-Login==0.6.3
Flask-Migrate==4.0.4
flask-restx==1.3.0
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.2
greenlet==3.1.1
importlib_resources==6.4.5
itsdangerous==2.2.0
Jinja2==3.1.4
jsonschema==4.23.0
jsonschema-specifications==2024.10.1
Mako==1.3.8
MarkupSafe==3.0.2
mysql-connector-python==8.0.33
mysqlclient==2.2.7
protobuf==3.20.3
PyJWT==2.10.1
PyMySQL==1.1.1
python-dotenv==1.0.0
pytz==2024.2
referencing==0.35.1
rpds-py==0.22.3
SQLAlchemy==2.0.36
typing_extensions==4.12.2
Werkzeug==3.1.3
WTForms==3.2.1""",
    "app": {
        "__init__.py": "",
        "models": {"__init__.py": "", "user.py": "", "todo.py": ""},
        "routes": {"__init__.py": "", "auth.py": "", "todo.py": "", "views.py": ""},
        "schemas": {"__init__.py": "", "user_schema.py": "", "todo_schema.py": ""},
        "utils": {"__init__.py": "", "auth_utils.py": ""}
        "forms": {"__init__.py": "", "login_form.py": "", "register_form.py": "", "todo_form.py": ""},
        "templates": {"base.html": "", "login.html": "", "register.html": "", "edit_todo.html": "", "home.html":"", "dashboard.html": "", "404.html":""},
        "static": {"style.css": "", "script.js": ""},
    },
    "run.py": ""
}

destination = Path.cwd()
create_flask_scaffold(destination, project_structure)
setup_virtualenv(destination)
```
