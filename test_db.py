from app.db.session import get_db_session, init_db
from app.services.user import UserService
from app.services.project import ProjectService
from app.services.task import TaskService

# جدول‌ها رو بساز
init_db()

with get_db_session() as db:
    # سرویس‌ها با session ساخته میشن
    user_service = UserService(db)
    project_service = ProjectService(db)
    task_service = TaskService(db)

    # اضافه کردن یک کاربر نمونه
    user = user_service.create_user(
        username="nazy",
        email="nazyhf@gmail.com",
        password="123456"
    )
    print("User added:", user.username)

    # اضافه کردن پروژه نمونه
    project = project_service.create_project(
        name="Sample Project",
        owner_id=user.id
    )
    print("Project added:", project.name)

    # اضافه کردن تسک نمونه
    task = task_service.create_task(
        title="Sample Task",
        project_id=project.id,
        assignee_id=user.id
    )
    print("Task added:", task.title)
