from typing import Optional
from datetime import datetime
from app.db.session import get_db_session, init_db
from app.services.user import UserService
from app.services.project import ProjectService
from app.services.task import TaskService
from app.models.task import TaskStatus, TaskPriority
from app.exceptions import TodoBaseException


class TodoCLI:
    """Command Line Interface for ToDo List application"""
    
    def __init__(self):
        self.current_user = None
        init_db()
    
    def run(self):
        """Main CLI loop"""
        print("=" * 50)
        print(" Welcome to ToDo List Application (Phase 2 - RDB)")
        print("=" * 50)
        
        while True:
            if self.current_user is None:
                self.show_auth_menu()
            else:
                self.show_main_menu()
    
    def show_auth_menu(self):
        """Show authentication menu"""
        print("\n--- Authentication ---")
        print("1. Register")
        print("2. Login")
        print("0. Exit")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            self.register()
        elif choice == '2':
            self.login()
        elif choice == '0':
            print("Goodbye!")
            exit(0)
        else:
            print("Invalid choice!")
    
    def show_main_menu(self):
        """Show main menu"""
        print(f"\n--- Main Menu (User: {self.current_user.username}) ---")
        print("1. Manage Projects")
        print("2. Manage Tasks")
        print("3. Logout")
        print("0. Exit")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            self.manage_projects()
        elif choice == '2':
            self.manage_tasks()
        elif choice == '3':
            self.logout()
        elif choice == '0':
            print("Goodbye!")
            exit(0)
        else:
            print("Invalid choice!")
    
    def register(self):
        """Register new user"""
        print("\n--- Register ---")
        username = input("Username: ").strip()
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        
        try:
            with get_db_session() as session:
                user_service = UserService(session)
                user = user_service.create_user(username, email, password)
                print(f"✓ User '{user.username}' registered successfully!")
        except TodoBaseException as e:
            print(f"✗ Error: {e.message}")
    
    def login(self):
        """Login user"""
        print("\n--- Login ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        try:
            with get_db_session() as session:
                user_service = UserService(session)
                user = user_service.authenticate(username, password)
                
                if user:
                    self.current_user = user
                    print(f"✓ Welcome back, {user.username}!")
                else:
                    print("✗ Invalid username or password!")
        except TodoBaseException as e:
            print(f"✗ Error: {e.message}")
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
        print("✓ Logged out successfully!")
    
    def manage_projects(self):
        """Manage user projects"""
    
if __name__ == "__main__":
    cli = TodoCLI()
    cli.run()
