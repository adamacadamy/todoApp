# TODO APP

A simple task management application that allows users to create, manage, and track tasks efficiently. This app provides authentication, task organization, and a user-friendly interface for seamless task handling.

## Table of Contents

1. [Description](#description)
2. [Installation](#installation)  
   1. [Clone the Repository](#1-clone-the-repository)  
   2. [Set Up the Virtual Environment](#2-set-up-the-virtual-environment)  
   3. [Install Dependencies](#3-install-the-dependencies)  
   4. [Set Up Environment Variables](#4-set-up-the-environment-variables)  
3. [Running the Application](#running-the-application)  
4. [Database Migrations](#database-migrations)  
5. [Project Structure](#project-structure)  
6. [Scaffold Script](#scaffold-script)  

---

## Description

The **TODO APP** is a web-based application built with Flask that allows users to manage their tasks. Users can:

- Register and log in securely.
- Create, update, and delete tasks.
- View all tasks on a user-friendly dashboard.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/todo-app.git
cd todo-app
```

### 2. Set Up the Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory of the project and add the following environment variables:

```text
SECRET_KEY=your_secret_key
DATABASE_URI=mysql+mysqlconnector://root:top!secret@localhost:3307/todo_db
FLASK_APP=run.py
FLASK_ENV=development
```

## Running the Application

1. **Activate the virtual environment**:

   ```bash
   source .venv/bin/activate
   ```

2. **Run the Flask application**:

   ```bash
   flask run
   ```

   The application will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Database Migrations

1. **Initialize the database migrations**:

   ```bash
   flask db init
   ```

2. **Create a new migration**:

   ```bash
   flask db migrate -m "Initial migration"
   ```

3. **Apply the migration**:

   ```bash
   flask db upgrade
   ```

## Project Structure

```text
todo-app/
├── .gitignore               # Ignore unnecessary files
├── .env                     # Environment variables
├── .vscode/                 # VSCode settings
│   ├── settings.json        # Workspace settings
│   └── launch.json          # Debugging configurations
├── app/                     # Application logic
│   ├── __init__.py          # Initialize Flask app
│   ├── utils/               # Utility functions
│   │   ├── __init__.py      # Package file
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
│   │   ├── home.html        # Home page
│   │   ├── dashboard.html   # Dashboard page
│   │   ├── edit_todo.html   # Edit ToDo page
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

## Scaffold Script

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

destination = Path.cwd()
create_flask_scaffold(destination, {})
setup_virtualenv(destination)
```
