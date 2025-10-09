from typing import List, Optional
import uuid
import sys
from datetime import datetime
from todolist.repository import InMemoryRepository
from todolist.service import ToDoListService, BusinessLogicError
from todolist.models.project import Project 
from todolist.models.task import TaskStatus 


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
        
def project_menu(service: ToDoListService):
    """Manages the loop for project operations."""
    while True:
        print_separator()
        print("--- Project Management ---")
        print("1. List All Projects")
        print("2. Create Project")
        print("3. Delete Project")
        print("4. Update Project (TODO)") # For brevity, we keep this as TODO
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
            elif choice == '5':
                break
            else:
                print("Invalid choice.")

        except BusinessLogicError as e:
            print(f"\n[❌ ERROR] Business Rule Violation: {e}")
        except Exception as e:
            print(f"\n[🚨 FATAL ERROR] An unexpected error occurred: {e}")



# 3. Task Menu (TODO)


def task_menu(service: ToDoListService):
    """Placeholder for Task Management Menu."""
    # This will be implemented next, focusing on:
    # 1. Selecting a project first.
    # 2. Creating a task (using parse_deadline).
    # 3. Listing tasks for the selected project.
    print("\nTask Management Menu is not yet implemented. Please select Project Management (1).")


if __name__ == "__main__":
    main()
    