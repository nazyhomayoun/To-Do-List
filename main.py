# main.py

"""
ToDo List Application - Phase 2 (RDB)
Main entry point for the application
"""


from app.cli.cli import TodoCLI


def main():
    # Main function to run the application
    cli = TodoCLI()
    cli.run()
    
if __name__ == "__main__":
    main()
