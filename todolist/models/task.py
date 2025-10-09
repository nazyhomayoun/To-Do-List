import uuid
from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    # keep task status data
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

class Task:
   # keep task data
    def __init__(self, project_id: uuid.UUID, title: str, description: str, deadline: datetime = None):
        self.id = uuid.uuid4()
        self.project_id = project_id # external key to project
        self.title = title
        self.description = description
        self.status: TaskStatus = TaskStatus.TODO
        self.deadline = deadline

    def __repr__(self):
        return f"Task(id='{self.id}', title='{self.title}', status='{self.status.value}')"