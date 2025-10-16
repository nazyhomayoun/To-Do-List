# ToDoList Project
# ToDoList (OOP & CLI)

A simple, command-line interface (CLI) based ToDoList management system, developed using Object-Oriented Programming (OOP) principles and a Layered Architecture in Python. This project uses Poetry for dependency management.

---

## Key Features

- **Project Management:** Create, view, update (name, description), and delete projects.  
- **Task CRUD Operations:** Create, list, update status (TODO, DOING, DONE), and delete tasks.  
- **Clean Architecture:** Clear separation of concerns between the CLI (User Interface), Service (Business Logic), and Repository (Data Management).  
- **Validations:** Enforces business constraints such as word limits, unique project names, and deadline format validation.  

---

## Prerequisites

- **Python:** Version 3.10 or higher.  
- **Poetry:** The dependency management tool.  

---

## Setup and Installation

To get the project running, you only need to install Poetry and then install the project dependencies.

### 1. Install Poetry

If you don't have Poetry installed, use the following command in your terminal (PowerShell/Bash):

```bash
curl -sSL https://install.python-poetry.org | python -
```

### 2. Install Dependencies

Navigate to the project's root directory (todolist_oop) and install the dependencies:

```bash
cd todolist_oop
poetry install
```

### Running the Application

Once installation is successful, run the application using the Poetry virtual environment:
```bash
poetry run python main.py
```
### Contribution:
If you find a bug or have a suggestion, feel free to create an Issue or submit a Pull Request on the develop branch.
