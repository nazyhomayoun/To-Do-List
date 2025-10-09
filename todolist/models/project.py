import uuid
from datetime import datetime

class Project:
    # keep project data
    def __init__(self, name: str, description: str):
        self.id = uuid.uuid4()
        self.name = name
        self.description = description
        self.created_at = datetime.now()

    # You can add additional methods or properties for Project below
    def __repr__(self):
        return f"Project(id='{self.id}', name='{self.name}')"
    