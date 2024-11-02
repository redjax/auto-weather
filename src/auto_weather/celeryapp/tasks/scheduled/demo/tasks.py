from celery.schedules import crontab


TASK_SCHEDULE_1m_say_hello = {
    "1m_say_hello": {
        "task": "say_hello",
        "schedule": crontab(minute="*"),
        "args": ["celery"],
    }
}
