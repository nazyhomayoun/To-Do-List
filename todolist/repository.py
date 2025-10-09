from todolist.models.project import Project
from todolist.models.task import Task
from typing import Dict, List, Optional
import uuid

class InMemoryRepository:
    """
    InMemoryRepository is a simple in-memory data storage layer for managing Project and Task objects.
    This repository provides basic CRUD operations.
    """
    
    def __init__(self):
        # use a dictionary to store objects to have O(1) access by ID.
        self._projects: Dict[uuid.UUID, Project] = {}
        self._tasks: Dict[uuid.UUID, Task] = {}


    # project's methods (CRUD)
   
    def add_project(self, project: Project) -> None:
        # add new project
        self._projects[project.id] = project

    def get_project_by_id(self, project_id: uuid.UUID) -> Optional[Project]:
        # return project by ID
        return self._projects.get(project_id)

    def get_all_projects(self) -> List[Project]:
        # return all projects
        return list(self._projects.values())

    def delete_project(self, project_id: uuid.UUID) -> None:
        # delete project
        self._projects.pop(project_id, None)
    
    def update_project(self, project: Project) -> None:
        # update project
        self._projects[project.id] = project


    # Task's methods (CRUD)


    def add_task(self, task: Task) -> None:
        # add new task
        self._tasks[task.id] = task

    def get_tasks_by_project_id(self, project_id: uuid.UUID) -> List[Task]:
        # return tasks by project ID
        return [task for task in self._tasks.values() if task.project_id == project_id]
    
    def get_task_by_id(self, task_id: uuid.UUID) -> Optional[Task]:
        # return task by ID
        return self._tasks.get(task_id)

    def update_task(self, task: Task) -> None:
        # update task
        self._tasks[task.id] = task

    def delete_task(self, task: Task) -> None:
        # delete task
        self._tasks.pop(task.id, None)