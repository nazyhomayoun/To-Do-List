"""
Scheduler for running periodic tasks
"""

import schedule # type: ignore
import time
from app.commands.autoclose_overdue import autoclose_overdue_tasks

def run_scheduler():
    """
    Run the scheduler with configured jobs
    """
    # Run autoclose every day at 00:00 (midnight)
    schedule.every().day.at("00:00").do(autoclose_overdue_tasks)
    
    # Or run every hour (for testing)
    # schedule.every().hour.do(autoclose_overdue_tasks)
    
    print("Scheduler started. Running autoclose overdue tasks...")
    print("Press Ctrl+C to stop.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\nScheduler stopped.")


if __name__ == "__main__":
    run_scheduler()
