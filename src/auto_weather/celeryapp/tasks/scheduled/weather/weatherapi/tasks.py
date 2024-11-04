from celery.schedules import crontab

TASK_SCHEDULE_15m_weatherapi_current_weather = {
    "15m_weatherapi_current_weather": {
        "task": "weatherapi-current-weather",
        "schedule": crontab(minute="*/15"),
    }
}