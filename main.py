from typing import List, Optional
import uuid
import sys
from datetime import datetime
from todolist.repository import InMemoryRepository
from todolist.service import ToDoListService, BusinessLogicError
from todolist.models.project import Project 
from todolist.models.task import Task, TaskStatus 


# Initialization & Main Loop
def initialize_app() -> ToDoListService:
    """Initializes the Repository and injects it into the Service layer."""

    repo = InMemoryRepository()
    service = ToDoListService(repository=repo)
    return service

def print_separator():
    """Prints a dividing line for better CLI readability."""
    print("-" * 50)

def main():
    """Main function to run the CLI application."""
    # Initialize the service layer
    try:
        service = initialize_app()
    except Exception as e:
        # Catch fatal errors during initialization (e.g., failed ENV loading)
        print(f"\n[FATAL ERROR] Application initialization failed: {e}")
        sys.exit(1)
        
    print("\n\n*** ToDoList Application Initialized Successfully ***")
    
    while True:
        print_separator()
        print("--- Main Menu ---")
        print("1. Manage Projects")
        print("2. Manage Tasks")
        print("3. Exit")
        print_separator()
        
        choice = input("Enter your choice (1-3): ")
        
        try:
            if choice == '1':
                project_menu(service)
            elif choice == '2':
                task_menu(service)
            elif choice == '3':
                print("Exiting application. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
                
        # Catch business rules errors raised by the Service layer
        except BusinessLogicError as e:
            print(f"\n[❌ ERROR] Business Rule Violation: {e}")
        # Catch unexpected errors
        except Exception as e:
            print(f"\n[🚨 FATAL ERROR] An unexpected error occurred: {e}")

# Helper Functions (Conversion)

def get_project_id_by_index(service: ToDoListService, index: int) -> Optional[uuid.UUID]:
    """Helper to get a Project ID based on a 1-based index from the list."""

    projects = service.get_all_projects()
    if 0 < index <= len(projects):
        # We need to sort or ensure order consistency if the repository doesn't guarantee it.
        # Here we just use the list order.
        return projects[index - 1].id
    return None

def parse_deadline(deadline_str: str) -> Optional[datetime]:

    """
    Tries to convert a string into a datetime object.
    This handles the Format Validation (Acceptance Criteria) at the CLI level.
    """

    if not deadline_str:
        return None
    try:
        return datetime.strptime(deadline_str.strip(), "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError("Invalid date format! Please use YYYY-MM-DD HH:MM.")
    return None

def list_projects(service: ToDoListService) -> List[Project]:
    """Retrieves and displays all projects."""

    projects = service.get_all_projects()
    if not projects:
        print("\n[INFO] No projects found.")
        return []
    
    print("\n--- Project List ---")
    for i, project in enumerate(projects):
        # Displaying only the first few chars of the UUID for readability
        tasks = service.get_tasks_for_project(project.id)
        done_tasks = [t for t in tasks if t.status == TaskStatus.DONE]
        
        print(f"  {i+1}. {project.name} (ID: {str(project.id)[:8]}...)")
        print(f"     Tasks: {len(done_tasks)}/{len(tasks)} done")
        
    print_separator()
    return projects

def create_project_cli(service: ToDoListService):
    """Handles user input and service call for creating a project."""

    print("\n--- Create New Project ---")
    name = input("Enter Project Name: ")
    description = input("Enter Project Description: ")
    
    # The service layer handles all validation (limit, uniqueness, word count)
    new_project = service.create_project(name=name, description=description)
    print(f"\n[✅ SUCCESS] Project '{new_project.name}' created with ID: {new_project.id}")

def delete_project_cli(service: ToDoListService):
    """Handles user input and service call for deleting a project (with cascade)."""

    projects = list_projects(service)
    if not projects:
        return

    choice = input("Enter the project NUMBER to delete, or 'B' to go back: ")
    if choice.upper() == 'B':
        return

    try:
        index = int(choice)
        project_id = get_project_id_by_index(service, index)
        
        if not project_id:
            print("[ERROR] Invalid project number.")
            return

        # Service handles the deletion and Cascade Delete logic
        service.delete_project(project_id)
        print(f"\n[✅ SUCCESS] Project #{index} and all its tasks have been deleted.")

    except ValueError:
        print("[ERROR] Invalid input. Please enter a number or 'B'.")
    
def update_project_cli(service: ToDoListService):
    """Handles user input and service call for updating a project."""
    projects = list_projects(service)
    if not projects:
        return

    choice = input("Enter the project NUMBER to update, or 'B' to go back: ")
    if choice.upper() == 'B':
        return

    try:
        index = int(choice)
        project_id = get_project_id_by_index(service, index)
        
        if not project_id:
            print("[❌ ERROR] Invalid project number.")
            return

        print("\n--- Update Project ---")
        
        # ignore null imput
        new_name = input(f"Enter New Project Name (Current: {projects[index-1].name}) [optional]: ")
        new_description = input(f"Enter New Description (Current: {projects[index-1].description}) [optional]: ")

        new_name = new_name.strip() if new_name else None
        new_description = new_description.strip() if new_description else None
        
        if not new_name and not new_description:
            print("[INFO] No changes specified.")
            return

        updated_project = service.update_project(
            project_id=project_id, 
            new_name=new_name, 
            new_description=new_description
        )
        print(f"\n[✅ SUCCESS] Project '{updated_project.name}' updated successfully.")

    except ValueError:
        print("[❌ ERROR] Invalid input. Please enter a number or 'B'.")
    
        
def project_menu(service: ToDoListService):
    """Manages the loop for project operations."""

    while True:
        print_separator()
        print("--- Project Management ---")
        print("1. List All Projects")
        print("2. Create Project")
        print("3. Delete Project")
        print("4. Update Project") 
        print("5. Back to Main Menu")
        print_separator()

        choice = input("Enter your choice (1-5): ")

        try:
            if choice == '1':
                list_projects(service)
            elif choice == '2':
                create_project_cli(service)
            elif choice == '3':
                delete_project_cli(service)
            elif choice == '4':
                update_project_cli(service)
            elif choice == '5':
                break
            else:
                print("Invalid choice.")

        except BusinessLogicError as e:
            print(f"\n[❌ ERROR] Business Rule Violation: {e}")
        except Exception as e:
            print(f"\n[🚨 FATAL ERROR] An unexpected error occurred: {e}")


def get_task_id_by_index(service: ToDoListService, project_id: uuid.UUID, index: int) -> Optional[uuid.UUID]:
    """Helper to get a Task ID based on a 1-based index from the list for a project."""

    tasks = service.get_tasks_for_project(project_id)
    if 0 < index <= len(tasks):
        return tasks[index - 1].id
    return None

def parse_deadline(deadline_str: str) -> Optional[datetime]:

    """
    Tries to convert a string into a datetime object.
    Raises ValueError on incorrect format (Acceptance Criteria).
    """

    if not deadline_str or deadline_str.strip() == '':
        return None
    try:
        # Expected format: YYYY-MM-DD HH:MM
        return datetime.strptime(deadline_str.strip(), "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError("Invalid date format! Please use YYYY-MM-DD HH:MM (e.g., 2025-12-31 14:30).")

def list_tasks(service: ToDoListService, project_id: uuid.UUID) -> List[Task]:
    """Retrieves and displays all tasks for the selected project."""

    tasks = service.get_tasks_for_project(project_id)
    
    if not tasks:
        print("\n[INFO] No tasks found for this project.")
        return []
        
    print("\n--- Task List ---")
    
    for i, task in enumerate(tasks):
        status_map = {
            TaskStatus.TODO: "◻️ TODO",
            TaskStatus.DOING: "⚙️ DOING",
            TaskStatus.DONE: "✅ DONE"
        }
        status_display = status_map.get(task.status, "[? UNKNOWN]")

        deadline_str = f"Deadline: {task.deadline.strftime('%Y-%m-%d %H:%M')}" if task.deadline else "No Deadline"
        
        print(f"  {i+1}. {status_display} | {task.title} (ID: {str(task.id)[:8]}... | {deadline_str})")
        
    print_separator()
    return tasks

# CRUD

def create_task_cli(service: ToDoListService, project_id: uuid.UUID):
    """Handles creating a new task."""
    print("\n--- Create New Task ---")
    title = input("Enter Task Title (max 30 words): ")
    description = input("Enter Task Description (max 150 words): ")
    
    # input deadline
    deadline_str = input("Enter Deadline (YYYY-MM-DD HH:MM) [optional]: ")
    
    try:
        deadline = parse_deadline(deadline_str)
        
        # Service handles business logic (limits, existence, future date)
        new_task = service.create_task(
            project_id=project_id, 
            title=title, 
            description=description, 
            deadline=deadline
        )
        print(f"\n[✅ SUCCESS] Task '{new_task.title}' created with status: TODO.")
        
    except ValueError as e:
        # Handle invalid deadline format
        print(f"\n[❌ ERROR] Validation Error: {e}")

def update_task_status_cli(service: ToDoListService, project_id: uuid.UUID):
    """Handles updating the status of an existing task."""

    tasks = list_tasks(service, project_id)
    if not tasks:
        return
    
    choice = input("Enter the task NUMBER to update its status, or 'B' to go back: ")
    if choice.upper() == 'B': return

    try:
        index = int(choice)
        task_id = get_task_id_by_index(service, project_id, index)
        
        if not task_id:
            print("[❌ ERROR] Invalid task number.")
            return

        print("\n--- Available Statuses ---")
        print("1. TODO")
        print("2. DOING")
        print("3. DONE")
        status_choice = input("Enter new status NUMBER (1-3): ")
        
        status_map = {'1': TaskStatus.TODO, '2': TaskStatus.DOING, '3': TaskStatus.DONE}
        new_status = status_map.get(status_choice)

        if not new_status:
             print("[❌ ERROR] Invalid status choice.")
             return

        updated_task = service.update_task(task_id=task_id, status=new_status)
        print(f"\n[✅ SUCCESS] Task '{updated_task.title}' updated to status: {updated_task.status.name}")

    except ValueError:
        print("[❌ ERROR] Invalid input.")

def delete_task_cli(service: ToDoListService, project_id: uuid.UUID):
    """Handles deleting a specific task."""
    tasks = list_tasks(service, project_id)
    if not tasks:
        return

    choice = input("Enter the task NUMBER to delete, or 'B' to go back: ")
    if choice.upper() == 'B': return

    try:
        index = int(choice)
        task_id = get_task_id_by_index(service, project_id, index)
        
        if not task_id:
            print("[❌ ERROR] Invalid task number.")
            return

        service.delete_task(task_id)
        print(f"\n[✅ SUCCESS] Task #{index} has been deleted.")

    except ValueError:
        print("[❌ ERROR] Invalid input. Please enter a number or 'B'.")

  
# 3. Task Menu 

def task_operation_menu(service: ToDoListService, project_id: uuid.UUID):
    """Main loop for CRUD operations on tasks within a selected project."""

    # Get project details
    project_details = service.get_project_details(project_id)

    while True:
        print_separator()
        print(f"--- Task Management for Project: {project_details.name} ---")
        print("1. List All Tasks")
        print("2. Create New Task")
        print("3. Update Task Status")
        print("4. Delete Task") 
        print("5. Back to Project Selection")
        print_separator()

        choice = input("Enter your choice (1-5): ")

        try:
            if choice == '1':
                list_tasks(service, project_id)
            elif choice == '2':
                create_task_cli(service, project_id)
            elif choice == '3':
                update_task_status_cli(service, project_id)
            elif choice == '4':
                delete_task_cli(service, project_id)
            elif choice == '5':
                break
            else:
                print("Invalid choice.")

        except BusinessLogicError as e:
            print(f"\n[❌ ERROR] Business Rule Violation: {e}")
        except Exception as e:
            print(f"\n[🚨 FATAL ERROR] An unexpected error occurred: {e}")

def task_menu(service: ToDoListService):
    """Manages the task operations by first selecting a project."""
    
    while True:
        # show project selection menu
        projects = list_projects(service) 
        if not projects:
            print("\n[INFO] Please create a project first before managing tasks.")
            return

        print("\n--- Select Project for Task Management ---")
        
        choice = input("Enter the project NUMBER to manage tasks for, or 'B' to go back: ")
        if choice.upper() == 'B':
            return

        try:
            index = int(choice)
            project_id = get_project_id_by_index(service, index)
            
            if not project_id:
                print("[❌ ERROR] Invalid project number.")
                continue
            
            task_operation_menu(service, project_id)

        except ValueError:
            print("[❌ ERROR] Invalid input. Please enter a number or 'B'.")
        except BusinessLogicError as e:
            print(f"\n[❌ ERROR] Business Rule Violation: {e}")


if __name__ == "__main__":
    main()
    