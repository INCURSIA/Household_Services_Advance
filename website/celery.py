from celery import Celery
from celery.schedules import crontab

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config["broker_url"],
        backend=app.config["result_backend"]
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """Ensure tasks run within Flask's app context."""
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    celery.conf.beat_schedule = {
        "daily-reminder-task": {
            "task": "website.tasks.send_daily_reminder",
            "schedule": crontab(hour=9, minute=0),  
        },
        "send-monthly-report-task": {
            "task": "website.tasks.send_monthly_report",
            "schedule": crontab(day_of_month=1, hour=0, minute=0), 
        }
    }
    celery.conf.timezone = "UTC"
    return celery
