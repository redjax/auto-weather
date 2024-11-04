from celery.schedules import crontab

TASK_SCHEDULE_15m_weatherapi_current_weather = {
    "15m_weatherapi_current_weather": {
        "task": "weatherapi-current-weather",
        "schedule": crontab(minute="*/15"),
    }
}

TASK_SCHEDULE_test_weatherapi_current_weather = {
    "test_weatherapi_current_weather": {
        "task": "weatherapi-current-weather",
        "schedule": crontab(minute="*"),
        "args": [True],
    }
}

TASK_SCHEDULE_30m_weatherapi_weather_forecast = {
    "30m_weatherapi_weather_forecast": {
        "task": "weatherapi-weather-forecast",
        "schedule": crontab(minute="*/30"),
        "args": [True],
    }
}
