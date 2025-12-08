# 📋 To-Do List Application

## ⚠️ DEPRECATION NOTICE

> **The CLI interface is being deprecated and will be removed in future versions.**
> 
> This project is transitioning to a **FastAPI-based web service**. 
> The CLI commands are no longer maintained and will be completely removed in version 3.0.0.

### 🚀 Quick Start (New Web API)
```bash
# Install dependencies
poetry install

# Run the server
poetry run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Access API documentation
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc

### 📦 Migration from CLI to API

| Old CLI Command | New API Endpoint |
|----------------|------------------|
| `Create new task` | `POST /api/v1/tasks/` |
| `View all tasks` | `GET /api/v1/tasks/` |
| `Update task` | `PUT /api/v1/tasks/{id}` |
| `Delete task` | `DELETE /api/v1/tasks/{id}` |
