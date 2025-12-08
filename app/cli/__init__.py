#Sfrom app.cli.main import TodoCLI

__all__ = ['TodoCLI']
"""
CLI Module - DEPRECATED

⚠️ This module is deprecated and will be removed in version 2.0.0

Please use the REST API instead:
    - Start server: uvicorn app.main:app --reload
    - API docs: http://localhost:8000/docs
"""

import warnings

warnings.warn(
    "The CLI module is deprecated. Use FastAPI REST API instead.",
    DeprecationWarning,
    stacklevel=2
)
