# main.py
"""
⚠️ DEPRECATION WARNING ⚠️

This CLI interface is deprecated and will be removed in future versions.
Please migrate to the FastAPI-based web service.

New usage:
    uvicorn app.main:app --reload

API docs: http://localhost:8000/docs
"""

import warnings

warnings.warn(
    "CLI interface is deprecated. Please use the FastAPI web service instead. "
    "Run: uvicorn app.main:app --reload",
    DeprecationWarning,
    stacklevel=2
)
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
