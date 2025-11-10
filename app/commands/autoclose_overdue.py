"""
Command to automatically close overdue tasks
"""

from datetime import datetime
from app.db.session import get_db_session
from app.services.task import TaskService


def autoclose_overdue_tasks():
    """
    Find and close all overdue tasks
    This command should be run periodically via cron or scheduler
    """
    with get_db_session() as session:
        task_service = TaskService(session)
        closed_count = task_service.close_overdue_tasks()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Autoclosed {closed_count} overdue task(s)")
        
        return closed_count


if __name__ == "__main__":
    autoclose_overdue_tasks()
