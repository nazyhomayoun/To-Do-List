# todolist/service.py

from todolist.repository import InMemoryRepository
from todolist.models.project import Project 
from todolist.models.task import Task, TaskStatus 
from typing import List, Optional
import uuid
from datetime import datetime

# Define a custom exception class for business logic errors
class BusinessLogicError(Exception):
    """ Used to handle business rules violations (e.g., duplicate name, invalid length). """
    pass

class ToDoListService:
    """
    The Business Logic Layer (Service).
    Responsible for enforcing rules, validation, and managing interaction with the Repository.
    """
    def __init__(self, repository: InMemoryRepository):
        # Dependency Injection: The service depends on the repository layer.
        self._repo = repository
    
    # Validation Helpers
    
    def _validate_project_name(self, name: str, project_id_to_ignore: uuid.UUID = None) -> None:
        # Checks if the project name is valid (word count, uniqueness).
        
        # 1. Validate word count (max 30 words based on requirements)
        if len(name.split()) > 30:
            raise BusinessLogicError("Project name must not exceed 30 words!")
            
        # 2. Validate uniqueness of the name
        all_projects = self._repo.get_all_projects()
        for project in all_projects:
            if project.name == name:
                raise BusinessLogicError(f"A project named '{name}' already exists.")

    # User Story: Create Project

    def create_project(self, name: str, description: str) -> Project:
        """ 
        Creates a new project after running business rules (validation). 
        """
        
        # Step 1: Execute business logic (validation)
        self._validate_project_name(name)
        if len(description.split()) > 150:
            raise BusinessLogicError("Project description must not exceed 150 words!")

        # Step 2: Create Model object (using the Models layer)
        new_project = Project(name=name, description=description)
        
        # Step 3: Save to Repository (using the Repository layer)
        self._repo.add_project(new_project)
        
        return new_project
    

    # User Story: Delete Project - (Includes Cascade Delete logic)
    
    def delete_project(self, project_id: uuid.UUID) -> None:
        """
        Deletes the project and all associated tasks (Cascade Delete).
        """
        
        # 1. Check if the project exists
        project_to_delete = self._repo.get_project_by_id(project_id)
        if not project_to_delete:
            raise BusinessLogicError(f"Project with ID {project_id} not found.")

        # 2. Execute business logic: Cascade Delete
        # Find all tasks related to this project
        related_tasks = self._repo.get_tasks_by_project_id(project_id)
        
        # Delete each related task from the Repository
        for task in related_tasks:
            self._repo.delete_task(task.id) 
            
        # 3. Delete the project itself
        self._repo.delete_project(project_id)

    # User Story: List Projects
    def get_all_projects(self) -> List[Project]:
        """
        Returns a list of all projects stored in the system.
        No business logic required here, just retrieval.
        """
        return self._repo.get_all_projects()

    def get_project_details(self, project_id: uuid.UUID) -> Project:
        """
        Returns a specific project object by its ID.
        Raises an error if the project is not found.
        """
        project = self._repo.get_project_by_id(project_id)
        if not project:
            raise BusinessLogicError(f"Project with ID {project_id} not found.")
        return project
    
    # User Story: Update Project
    def update_project(self, project_id: uuid.UUID, new_name: str, new_description: str) -> Project:
        # update project details

        # 1. Check if the project exists
        project_to_update = self._repo.get_project_by_id(project_id)
        if not project_to_update:
            raise BusinessLogicError(f"Project with ID {project_id} not found.")

        # 2. Execute business logic (Validation)
        # Validate the new name, ignoring the current project ID
        self._validate_project_name(new_name, project_id_to_ignore=project_id)

        if len(new_description.split()) > 150:
            raise BusinessLogicError("Project description must not exceed 150 words!")

        # 3. Update the model object (Mutating the object)
        project_to_update.name = new_name
        project_to_update.description = new_description
        
        # 4. Save the updated object to the Repository (Repository will overwrite the existing entry)
        self._repo.update_project(project_to_update)
        
        return project_to_update

    # User Story: Create Task (Start of Task CRUD)
    
    def create_task(self, project_id: uuid.UUID, title: str, description: str, deadline: datetime = None) -> Task:
        """
        Creates a new task associated with a specific project.
        Requires validation that the parent project exists.
        """

        # 1. Validation: Ensure the parent project exists
        parent_project = self._repo.get_project_by_id(project_id)
        if not parent_project:
            raise BusinessLogicError(f"Cannot create task. Project with ID {project_id} does not exist.")

        # 2. Validation: Task title/description word limits
        if len(title.split()) > 30:
            raise BusinessLogicError("Task title must not exceed 30 words.")
        if len(description.split()) > 150:
            raise BusinessLogicError("Task description must not exceed 150 words.")

        # 3. Create Model object
        new_task = Task(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline
        )

        # 4. Save to Repository
        self._repo.add_task(new_task)

        return new_task
    # User Story: Read Task

    # User Story: List Tasks (Read)


    def get_tasks_for_project(self, project_id: uuid.UUID) -> List[Task]:
        """
        Retrieves all tasks associated with a specific project ID.
        Requires validation that the parent project exists.
        """
        # 1. Validation: Ensure the parent project exists
        if not self._repo.get_project_by_id(project_id):
            raise BusinessLogicError(f"Project with ID {project_id} does not exist.")

        # 2. Retrieve tasks from the Repository
        return self._repo.get_tasks_by_project_id(project_id)

    # User Story: Update Task


    def update_task(self, 
                    task_id: uuid.UUID, 
                    title: Optional[str] = None, 
                    description: Optional[str] = None, 
                    status: Optional[TaskStatus] = None) -> Task:
        """
        Updates the details of an existing task.
        Performs validation on updated fields (title length, valid status).
        """
        # 1. Check if the task exists
        task_to_update = self._repo.get_task_by_id(task_id)
        if not task_to_update:
            raise BusinessLogicError(f"Task with ID {task_id} not found.")

        # 2. Apply updates and run Validation
        if title is not None:
            if len(title.split()) > 30:
                raise BusinessLogicError("Task title must not exceed 30 words.")
            task_to_update.title = title
            
        if description is not None:
            # TODO: Add validation for description (max 150 words) here.
            task_to_update.description = description

        if status is not None:
            # The enum ensures the status is valid, but we check if the provided value is a TaskStatus instance.
            if not isinstance(status, TaskStatus):
                 raise BusinessLogicError("Invalid status provided. Must be 'TODO', 'DOING', or 'DONE'.")
            task_to_update.status = status

        # 3. Save the updated object to the Repository
        self._repo.update_task(task_to_update)
        
        return task_to_update

    # User Story: Delete Task


    def delete_task(self, task_id: uuid.UUID) -> None:
        """
        Deletes a specific task by its ID.
        """
        # 1. Check if the task exists before deleting (optional, but good practice)
        if not self._repo.get_task_by_id(task_id):
            # We could raise an error here, but for deletion, often we just proceed 
            # as the Repository's pop(id, None) handles the non-existence gracefully.
            # However, for a user-facing action, giving feedback is better:
            raise BusinessLogicError(f"Task with ID {task_id} not found.")
            
        # 2. Delete from Repository
        self._repo.delete_task(task_id)
