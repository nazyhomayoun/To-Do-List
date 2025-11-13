from app.db import SessionLocal, engine
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.services.project import ProjectService
from sqlalchemy.exc import SQLAlchemyError

# اتصال به دیتابیس
session = SessionLocal()

try:
    print("✅ Connection successful")

    # --- 1️⃣ اضافه کردن کاربر ---
    user = User(username="nazy_test", email="nazy@example.com", password_hash="hashedpass")
    session.add(user)
    session.commit()
    print(f"👤 User added: {user.username} (id={user.id})")

    # --- 2️⃣ اضافه کردن پروژه ---
    project_service = ProjectService(session)
    project = project_service.create_project(
        title="Sample Project",
        description="Test project for database check",
        owner_id=user.id   # حالا متد این پارامتر رو می‌پذیره
    )
    session.commit()
    print(f"📁 Project added: {project.title} (id={project.id})")

    # --- 3️⃣ اضافه کردن تسک ---
    task = Task(
        title="First Task",
        description="This is a test task for the project",
        project_id=project.id
    )
    session.add(task)
    session.commit()
    print(f"✅ Task added: {task.title} (id={task.id})")

except SQLAlchemyError as e:
    print("❌ Database error:", e)
    session.rollback()

finally:
    session.close()
    print("🔚 Test finished")
