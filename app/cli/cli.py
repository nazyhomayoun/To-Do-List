# app/cli/cli.py (continued)

import sys
from datetime import datetime
from typing import Optional
from app.db.session import get_db_session, init_db
from app.services.user import UserService
from app.services.project import ProjectService
from app.services.task import TaskService
from app.models.task import TaskStatus, TaskPriority
from app.exceptions.base import (
    TodoBaseException,
    NotFoundException,
    ValidationException,
    DuplicateException
)


class TodoCLI:
    def __init__(self):
        self.current_user = None
        self.user_service = None
        self.project_service = None
        self.task_service = None

    def initialize_services(self, session):
        """Initialize all services with database session"""
        self.user_service = UserService(session)
        self.project_service = ProjectService(session)
        self.task_service = TaskService(session)

    def clear_screen(self):
        """Clear console screen"""
        print("\n" * 50)

    def display_header(self, title: str):
        """Display section header"""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60 + "\n")

    def get_input(self, prompt: str, required: bool = True) -> Optional[str]:
        """Get user input with validation"""
        while True:
            value = input(prompt).strip()
            if value or not required:
                return value if value else None
            print("This field is required!")

    def run(self):
        """Main application loop"""
        try:
            # Initialize database
            init_db()
            print("Welcome to ToDo List Application!")
            print("-" * 60)
            
            with get_db_session() as session:
                self.initialize_services(session)
                
                while True:
                    if not self.current_user:
                        self.auth_menu()
                    else:
                        self.main_menu()
                        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\nCritical Error: {e}")
            sys.exit(1)

    def auth_menu(self):
        """Authentication menu"""
        self.display_header("Authentication")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        
        choice = self.get_input("\nSelect an option: ")
        
        if choice == "1":
            self.register()
        elif choice == "2":
            self.login()
        elif choice == "3":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option!")

    def register(self):
        """User registration"""
        self.display_header("Register New User")
        
        try:
            email = self.get_input("Email: ")
            password = self.get_input("Password: ")
            first_name = self.get_input("First Name: ")
            last_name = self.get_input("Last Name: ")
            
            user = self.user_service.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            print(f"\n✓ User registered successfully! Welcome {user.first_name}!")
            self.current_user = user
            
        except DuplicateException as e:
            print(f"\n✗ Error: {e}")
        except ValidationException as e:
            print(f"\n✗ Validation Error: {e}")
        except TodoBaseException as e:
            print(f"\n✗ Error: {e}")

    def login(self):
        """User login"""
        self.display_header("Login")
        
        try:
            email = self.get_input("Email: ")
            password = self.get_input("Password: ")
            
            user = self.user_service.authenticate(email, password)
            
            if user:
                self.current_user = user
                print(f"\n✓ Welcome back, {user.first_name}!")
            else:
                print("\n✗ Invalid email or password!")
                
        except NotFoundException as e:
            print(f"\n✗ Error: {e}")
        except TodoBaseException as e:
            print(f"\n✗ Error: {e}")

    def logout(self):
        """User logout"""
        if self.current_user:
            print(f"\nGoodbye, {self.current_user.first_name}!")
            self.current_user = None
        else:
            print("\nYou are not logged in!")

    def main_menu(self):
        """Main application menu"""
        self.display_header(f"Main Menu - Hello {self.current_user.first_name}!")
        print("1. Manage Projects")
        print("2. Manage Tasks")
        print("3. View All My Tasks")
        print("4. Close Overdue Tasks")
        print("5. Logout")
        print("6. Exit")
        
        choice = self.get_input("\nSelect an option: ")
        
        if choice == "1":
            self.project_menu()
        elif choice == "2":
            self.task_menu()
        elif choice == "3":
            self.view_all_tasks()
        elif choice == "4":
            self.close_overdue_tasks()
        elif choice == "5":
            self.logout()
        elif choice == "6":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option!")

    # ==================== PROJECT MANAGEMENT ====================

    def project_menu(self):
        """Project management menu"""
        self.display_header("Project Management")
        print("1. Create Project")
        print("2. List My Projects")
        print("3. View Project Details")
        print("4. Update Project")
        print("5. Delete Project")
        print("6. Back to Main Menu")
        
        choice = self.get_input("\nSelect an option: ")
        
        if choice == "1":
            self.create_project()
        elif choice == "2":
            self.list_projects()
        elif choice == "3":
            self.view_project_details()
        elif choice == "4":
            self.update_project()
        elif choice == "5":
            self.delete_project()
        elif choice == "6":
            return
        else:
            print("Invalid option!")

    def create_project(self):
        """Create new project"""
        self.display_header("Create New Project")
        
        try:
            title = self.get_input("Project Title: ")
            description = self.get_input("Description (optional): ", required=False)
            
            project = self.project_service.create_project(
                user_id=self.current_user.id,
                title=title,
                description=description
            )
            
            print(f"\n✓ Project '{project.title}' created successfully!")
            
        except ValidationException as e:
            print(f"\n✗ Validation Error: {e}")
        except TodoBaseException as e:
            print(f"\n✗ Error: {e}")

    def list_projects(self):
        """List all user projects"""
        self.display_header("My Projects")
        
        try:
            projects = self.project_service.get_user_projects(self.current_user.id)
            
            if not projects:
                print("No projects found. Create your first project!")
                return
            
            for idx, project in enumerate(projects, 1):
                task_count = len(project.tasks)
                print(f"{idx}. [{project.id}] {project.title}")
                print(f"   Description: {project.description or 'N/A'}")
                print(f"   Tasks: {task_count}")
                print(f"   Created: {project.created_at.strftime('%Y-%m-%d %H:%M')}")
                print("-" * 60)
                
        except TodoBaseException as e:
            print(f"\n✗ Error: {e}")

    def view_project_details(self):
        """View detailed project information"""
        self.display_header("Project Details")
        
        try:
            project_id = int(self.get_input("Enter Project ID: "))
            project = self.project_service.get_project_with_tasks(project_id)
            
            # Verify ownership
            if project.user_id != self.current_user.id:
                print("\n✗ You don't have permission to view this project!")
                return
            
            print(f"\nTitle: {project.title}")
            print(f"Description: {project.description or 'N/A'}")
            print(f"Created: {project.created_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"Updated: {project.updated_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"\nTotal Tasks: {len(project.tasks)}")
            
            if project.tasks:
                print("\n--- Tasks ---")
                for task in project.tasks:
                    status_emoji = {
                        TaskStatus.TODO: "⭕",
                        TaskStatus.IN_PROGRESS: "🔄",
                        TaskStatus.DONE: "✅",
                        TaskStatus.CANCELLED: "❌",
                        TaskStatus.OVERDUE: "⏰"
                    }.get(task.status, "⭕")
                    
                    print(f"  {status_emoji} [{task.id}] {task.title}")
                    print(f"     Status: {task.status.value} | Priority: {task.priority.value}")
                    if task.deadline:
                        print(f"     Deadline: {task.deadline.strftime('%Y-%m-%d')}")
            
        except ValueError:
            print("\n✗ Invalid Project ID!")
        except NotFoundException as e:
            print(f"\n✗ Error: {e}")
        except TodoBaseException as e:
            print(f"\n✗ Error: {e}")

    def update_project(self):
        """Update project information"""
        self.display_header("Update Project")
        
        try:
            project_id = int(self.get_input("Enter Project ID: "))
            project = self.project_service.get_project_by_id(project_id)
            
            # Verify ownership
            if project.user_id != self.current_user.id:
                print("\n✗ You don't have permission to update this project!")
                return
            
            print(f"\nCurrent Title: {project.title}")
            print(f"Current Description: {project.description or 'N/A'}")
            
            new_title = self.get_input("\nNew Title (press Enter to keep current): ", required=False)
            new_description = self.get_input("New Description (press Enter to keep current): ", required=False)
            
            updated_project = self.project_service.update_project(
                project_id=project_id,
                title=new_title if new_title else None,
                description=new_description if new_description else None
            )
            
            print(f"\n✓ Project updated successfully!")
            
        except ValueError:
            print("\n✗ Invalid Project ID!")
        except NotFoundException as e:
            print(f"\n✗ Error: {e}")
        except TodoBaseException as e:
            print(f"\n✗ Error: {e}")

    def delete_project(self):
        """Delete a project"""
        self.display_header("Delete Project")
        
        try:
            project_id = int(self.get_input("Enter Project ID: "))
            project = self.project_service.get_project_by_id(project_id)
            
            # Verify ownership
            if project.user_id != self.current_user.id:
                print("\n✗ You don't have permission to delete this project!")
                return
            
            confirm = self.get_input(
                f"\n⚠ Are you sure you want to delete '{project.title}' and all its tasks? (yes/no): "
            )
            
            if confirm.lower() == 'yes':
                self.project_service.delete_project(project_id)
                print(f"\n✓ Project deleted successfully!")
            else:
                print("\nDeletion cancelled.")
                
        except ValueError:
            print("\n✗ Invalid Project ID!")
        except NotFoundException as e:
            print(f"\n✗ Error: {e}")
        except TodoBaseException as e:
            print(f"\n✗ Error: {e}")

    # ==================== TASK MANAGEMENT ====================

    def task_menu(self):
        """Task management menu"""
        self.display_header("Task Management")
        print("1. Create Task")
        print("2. List Project Tasks")
        print("3. View Task Details")
        print("4. Update Task")
        print("5. Change Task Status")
        print("6. Delete Task")
        print("7. Back to Main Menu")
        
        choice = self.get_input("\nSelect an option: ")
        
        if choice == "1":
            self.create_task()
        elif choice == "2":
            self.list_project_tasks()
        elif choice == "3":
            self.view_task_details()
        elif choice == "4":
            self.update_task()
        elif choice == "5":
            self.change_task_status()
        elif choice == "6":
            self.delete_task()
        elif choice == "7":
            return
        else:
            print("Invalid option!")

    def create_task(self):
        """Create new task"""
        self.display_header("Create New Task")
        
        try:
            # First, show user's projects
            projects = self.project_service.get_user_projects(self.current_user.id)
            
            if not projects:
                print("You don't have any projects. Please create a project first!")
                return
            
            print("Your Projects:")
            for idx, project in enumerate(projects, 1):
                print(f"{idx}. [{project.id}] {project.title}")
            
            project_id = int(self.get_input("\nEnter Project ID: "))
            
            # Verify project ownership
            project = self.project_service.get_project_by_id(project_id)
            if project.user_id != self.current_user.id:
                print("\n✗ Invalid project!")
                return
            
            title = self.get_input("Task Title: ")
            description = self.get_input("Description (optional): ", required=False)
            
            # Priority
            print("\nPriority:")
            for idx, priority in enumerate(TaskPriority, 1):
                print(f"{idx}. {priority.value}")
            priority_choice = int(self.get_input("Select Priority (1-3): "))
            priority = list(TaskPriority)[priority_choice - 1]
            
            # Deadline
            deadline_str = self.get_input("Deadline (YYYY-MM-DD, optional): ", required=False)
            deadline = None
            if deadline_str:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
            
            task = self.task_service.create_task(
                project_id=project_id,
                title=title,
                description=description,
                priority=priority,
                deadline=deadline
            )
            
            print(f"\n✓ Task '{task.title}' created successfully!")
            
        except ValueError as e:
            print(f"\n✗ Invalid input: {e}")
        except ValidationException as e:
            print(f"\n✗ Validation Error: {e}")
        except TodoBaseException as e:
            print(f"\n✗ Error: {e}")

    def list_project_tasks(self):
        """List tasks for a specific project"""
        self.display_header("Project Tasks")
        
        try:
            project_id = int(self.get_input("Enter Project ID: "))
            project = self.project_service.get_project_with_tasks(project_id)
            
            # Verify ownership
            if project.user_id != self.current_user.id:
                print("\n✗ You don't have permission to view this project!")
                return
            
            print(f"\nProject: {project.title}")
            print(f"Total Tasks: {len(project.tasks)}\n")
            
            if not project.tasks:
                print("No tasks found in this project.")
                return
            
            for task in project.tasks:
                status_emoji = {
                    TaskStatus.TODO: "⭕",
                    TaskStatus.IN_PROGRESS: "🔄",
                    TaskStatus.DONE: "✅",
                    TaskStatus.CANCELLED: "❌",
                    TaskStatus.OVERDUE: "⏰"
                }.get(task.status, "⭕")
                
                print(f"{status_emoji} [{task.id}] {task.title}")
                print(f"   Status: {task.status.value} | Priority: {task.priority.value}")
                if task.deadline:
                    deadline_str = task.deadline.strftime('%Y-%m-%d')
                    if task.is_overdue():
                        print(f"   Deadline: {deadline_str} ⚠️ OVERDUE")
                    else:
                        print(f"   Deadline: {deadline_str}")
                print("-" * 60)
                
        except ValueError:
            print("\n✗ Invalid Project ID!")
        except NotFoundException as e:
            print(f"\n✗ Error: {e}")
        except TodoBaseException as e:
            print(f"\n✗ Error: {e}")

    def view_task_details(self):
        """View detailed task information"""
        self.display_header("Task Details")
        
        try:
            task_id = int(self.get_input("Enter Task ID: "))
            task = self.task_service.get_task_by_id(task_id)
            
            # Verify ownership through project
            project = self.project_service.get_project_by_id(task.project_id)
            if project.user_id != self.current_user.id:
                print("\n✗ You don't have permission to view this task!")
                return
            
            print(f"\nTitle: {task.title}")
            print(f"Description: {task.description or 'N/A'}")
            print(f"Status: {task.status.value}")
            print(f"Priority: {task.priority.value}")
            print(f"Project: {project.title}")
            if task.deadline:
                print(f"Deadline: {task.deadline.strftime('%Y-%m-%d')}")
                if task.is_overdue():
                    print("⚠️ This task is OVERDUE!")
            print(f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"Updated: {task.updated_at.strftime('%Y-%m-%d %H:%M')}")
            
        except ValueError:
            print("\n✗ Invalid Task ID!")
        except NotFoundException as e:
            print(f"\n✗ Error: {e}")
        except TodoBaseException as e:
            print(f"\n✗ Error: {e}")

    def update_task(self):
        """Update task information"""
        self.display_header("Update Task")
        
        try:
            task_id = int(self.get_input("Enter Task ID: "))
            task = self.task_service.get_task_by_id(task_id)
            
            # Verify ownership
            project = self.project_service.get_project_by_id(task.project_id)
            if project.user_id != self.current_user.id:
                print("\n✗ You don't have permission to update this task!")
                return
            
            print(f"\nCurrent Title: {task.title}")
            print(f"Current Description: {task.description or 'N/A'}")
            print(f"Current Priority: {task.priority.value}")
            if task.deadline:
                print(f"Current Deadline: {task.deadline.strftime('%Y-%m-%d')}")
            
            new_title = self.get_input("\nNew Title (press Enter to keep current): ", required=False)
            new_description = self.get_input("New Description (press Enter to keep current): ", required=False)
            
            # Priority
            change_priority = self.get_input("Change Priority? (yes/no): ")
            new_priority = None
            if change_priority.lower() == 'yes':
                print("\nPriority:")
                for idx, priority in enumerate(TaskPriority, 1):
                    print(f"{idx}. {priority.value}")
                priority_choice = int(self.get_input("Select Priority (1-3): "))
                new_priority = list(TaskPriority)[priority_choice - 1]
            
            # Deadline
            change_deadline = self.get_input("Change Deadline? (yes/no): ")
            new_deadline = None
            if change_deadline.lower() == 'yes':
                deadline_str = self.get_input("New Deadline (YYYY-MM-DD): ")
                if deadline_str:
                    new_deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
            
            updated_task = self.task_service.update_task(
                task_id=task_id,
                title=new_title if new_title else None,
                description=new_description if new_description else None,
                priority=new_priority,
                deadline=new_deadline
            )
            
            print(f"\n✓ Task updated successfully!")
            
        except ValueError as e:
            print(f"\n✗ Invalid input: {e}")
        except NotFoundException as e:
            print(f"\n✗ Error: {e}")
        except TodoBaseException as e:
            print(f"\n✗ Error: {e}")

    def change_task_status(self):
        """Change task status"""
        self.display_header("Change Task Status")
        
        try:
            task_id = int(self.get_input("Enter Task ID: "))
            task = self.task_service.get_task_by_id(task_id)
            
            # Verify ownership
            project = self.project_service.get_project_by_id(task.project_id)
            if project.user_id != self.current_user.id:
                print("\n✗ You don't have permission to update this task!")
                return
            
            print(f"\nCurrent Status: {task.status.value}")
            print("\nAvailable Statuses:")
            for idx, status in enumerate(TaskStatus, 1):
                print(f"{idx}. {status.value}")
            
            status_choice = int(self.get_input("\nSelect New Status (1-5): "))
            new_status = list(TaskStatus)[status_choice - 1]
            
            updated_task = self.task_service.update_task_status(task_id, new_status)
            print(f"\n✓ Task status changed to '{new_status.value}'!")
            
        except ValueError as e:
            print(f"\n✗ Invalid input: {e}")
        except NotFoundException as e:
            print(f"\n✗ Error: {e}")
        except TodoBaseException as e:
            print(f"\n✗ Error: {e}")

    def delete_task(self):
        """Delete a task"""
        self.display_header("Delete Task")
        
        try:
            task_id = int(self.get_input("Enter Task ID: "))
            task = self.task_service.get_task_by_id(task_id)
            
            # Verify ownership
            project = self.project_service.get_project_by_id(task.project_id)
            if project.user_id != self.current_user.id:
                print("\n✗ You don't have permission to delete this task!")
                return
            
            confirm = self.get_input(
                f"\n⚠ Are you sure you want to delete '{task.title}'? (yes/no): "
            )
            
            if confirm.lower() == 'yes':
                self.task_service.delete_task(task_id)
                print(f"\n✓ Task deleted successfully!")
            else:
                print("\nDeletion cancelled.")
                
        except ValueError:
            print("\n✗ Invalid Task ID!")
        except NotFoundException as e:
            print(f"\n✗ Error: {e}")
        except TodoBaseException as e:
            print(f"\n✗ Error: {e}")

    def view_all_tasks(self):
        """View all tasks across all projects"""
        self.display_header("All My Tasks")
        
        try:
            projects = self.project_service.get_user_projects(self.current_user.id)
            
            if not projects:
                print("You don't have any projects yet.")
                return
            
            total_tasks = 0
            for project in projects:
                if project.tasks:
                    print(f"\n📁 Project: {project.title}")
                    print("-" * 60)
                    for task in project.tasks:
                        total_tasks += 1
                        status_emoji = {
                            TaskStatus.TODO: "⭕",
                            TaskStatus.IN_PROGRESS: "🔄",
                            TaskStatus.DONE: "✅",
                            TaskStatus.CANCELLED: "❌",
                            TaskStatus.OVERDUE: "⏰"
                        }.get(task.status, "⭕")
                        
                        print(f"  {status_emoji} [{task.id}] {task.title}")
                        print(f"     Status: {task.status.value} | Priority: {task.priority.value}")
                        if task.deadline:
                            deadline_str = task.deadline.strftime('%Y-%m-%d')
                            if task.is_overdue():
                                print(f"     Deadline: {deadline_str} ⚠️ OVERDUE")
                            else:
                                print(f"     Deadline: {deadline_str}")
            
            print(f"\n{'=' * 60}")
            print(f"Total Tasks: {total_tasks}")
            
        except TodoBaseException as e:
            print(f"\n✗ Error: {e}")

    def close_overdue_tasks(self):
        """Manually close all overdue tasks"""
        self.display_header("Close Overdue Tasks")
        
        try:
            closed_count = self.task_service.close_overdue_tasks()
            
            if closed_count > 0:
                print(f"\n✓ Successfully closed {closed_count} overdue task(s)!")
            else:
                print("\n✓ No overdue tasks found!")
                
        except TodoBaseException as e:
            print(f"\n✗ Error: {e}")
