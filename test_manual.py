# test_manual.py

import sys
from datetime import datetime, timedelta
from app.db.session import get_db_session, init_db
from app.services.user import UserService
from app.services.project import ProjectService
from app.services.task import TaskService
from app.models.task import TaskStatus, TaskPriority


def test_full_scenario():
    print("=" * 70)
    print("Starting test and creating sample data")
    print("=" * 70)

    init_db()

    with get_db_session() as session:
        user_service = UserService(session)
        project_service = ProjectService(session)
        task_service = TaskService(session)

        # =====================================================
        # 1. USERS
        # =====================================================
        print("\n[1] Creating Users\n" + "-" * 70)

        def get_or_create_user(username, email, password):
            from app.models.user import User

            # اول چک کن وجود داره یا نه
            existing_user = session.query(User).filter_by(email=email).first()
            if existing_user:
                print(f"⚠️  User already exists: {existing_user.username}")
                return existing_user

            # اگه نبود، بساز
            try:
                new_user = user_service.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                print(f"✅ User created: {new_user.username}")
                return new_user
            except Exception as e:
                print(f"❌ Error creating user: {e}")
                raise

        user1 = get_or_create_user("lili_meri", "lili.meri@example.com", "123456")
        print(f"User OK → {user1.username}")

        # =====================================================
        # 2. PROJECTS
        # =====================================================
        print("\n[2] Creating Projects\n" + "-" * 70)

        project1 = project_service.create_project(
            title="shopping",
            owner_id=user1.id,
            description="Buy a jacket"
        )
        project2 = project_service.create_project(
            title="Database Performance Optimization",
            owner_id=user1.id,
            description="improve queries",
        )
        print("Projects created successfully.")

        # =====================================================
        # 3. TASKS (with assignee_id )
        # =====================================================
        print("\n[3] Creating Tasks\n" + "-" * 70)

        def create_task(**kwargs):
            task = task_service.create_task(**kwargs)
            print(f"   ✓ Task: {task.title} | Assigned to {task.assignee.username}")
            return task

        # Project 1 tasks – assign to user1
        task1 = create_task(
            title="shopping",
            project_id=project1.id,
            assignee_id=user1.id,
            description="need to buy new jacket",
            priority=TaskPriority.MEDIUM,
            deadline=datetime.now() + timedelta(days=7)
        )


        # Overdue tasks
        task2 = create_task(
            title="Database Performance Optimization",
            project_id=project1.id,
            assignee_id=user1.id,
            description="Optimize queries",
            priority=TaskPriority.HIGH,
            deadline=datetime.now() - timedelta(days=3)
        )

        # =====================================================
        # 4. STATUS UPDATES
        # =====================================================
        print("\n[4] Updating Task Status\n" + "-" * 70)

        task_service.change_task_status(task1.id, TaskStatus.DONE)
        task_service.change_task_status(task2.id, TaskStatus.IN_PROGRESS)
        print("Statuses updated.")

        # =====================================================
        # 5. SUMMARY
        # =====================================================
        print("\n[5] Data Summary\n" + "=" * 70)

        projects = project_service.get_all_projects()

        for p in projects:
            tasks = task_service.get_project_tasks(p.id)
            print(f"\n📁 {p.title} | {len(tasks)} Tasks")
            for t in tasks:
                print(f"    - {t.title} [{t.status}] → assignee:{t.assignee.username}")

        # =====================================================
        # 6. Auto-close overdue
        # =====================================================
        print("\n[6] Closing Overdue Tasks\n" + "-" * 70)

        closed = task_service.close_overdue_tasks()
        print(f"Closed {closed} overdue tasks.")

        print("\nTEST COMPLETED SUCCESSFULLY 🎉")


if __name__ == "__main__":
    try:
        test_full_scenario()
    except Exception as e:
        print("\n❌ Error running test:", e)
        import traceback
        traceback.print_exc()
        sys.exit(1)