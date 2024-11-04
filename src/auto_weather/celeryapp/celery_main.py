from __future__ import annotations

from auto_weather.celeryapp.tasks.scheduled.demo import TASK_SCHEDULE_1m_say_hello
from auto_weather.celeryapp.tasks.scheduled.weather.weatherapi import (
    TASK_SCHEDULE_15m_weatherapi_current_weather,
    TASK_SCHEDULE_30m_weatherapi_weather_forecast,
    TASK_SCHEDULE_test_weatherapi_current_weather,
)

from .settings import BACKEND_URL, BROKER_URL, CELERY_SETTINGS

from celery import Celery, current_app
from celery.result import AsyncResult
from loguru import logger as log

log.add("logs/celery.log", rotation="15 MB", retention=3)
log.add("logs/celery.error.log", rotation="15 MB", retention=3, level="ERROR")

INCLUDE_TASK_PATHS = [
    "auto_weather.celeryapp.tasks.scheduled",
    "auto_weather.celeryapp.tasks.adhoc",
]

celery_app = Celery(
    "auto_weather.celeryapp",
    broker=BROKER_URL,
    backend=BACKEND_URL,
    include=INCLUDE_TASK_PATHS,
)

celery_app.conf.update(
    timzone=CELERY_SETTINGS.get("CELERY_TZ", default="Etc/UTC"), enable_utc=True
)

celery_app.autodiscover_tasks(INCLUDE_TASK_PATHS)


def print_discovered_tasks() -> list[str]:
    current_app.loader.import_default_modules()

    tasks: list[str] = list(
        sorted(name for name in current_app.tasks if not name.startswith("celery."))
    )

    print(f"Discovered [{len(tasks)}] Celery task(s): {[t for t in tasks]}")

    return tasks


## Periodic jobs
@celery_app.on_after_finalize.connect
def scheduled_tasks(sender, **kwargs):
    if not sender:
        ## This line is so vulture stops warning on unused variable 'sender'
        pass

    if not kwargs:
        ## This line is so vulture stops warning on unused variable 'kwargs'
        pass

    ## Configure celery beat schedule
    celery_app.conf.beat_schedule = {
        **TASK_SCHEDULE_1m_say_hello,
        **TASK_SCHEDULE_15m_weatherapi_current_weather,
        **TASK_SCHEDULE_30m_weatherapi_weather_forecast,
        ## Uncomment to get current weather every minute
        # **TASK_SCHEDULE_test_weatherapi_current_weather,
    }


print_discovered_tasks()


def check_task(task_id: str = None, app: Celery = celery_app) -> AsyncResult | None:
    """Check a Celery task by its ID.

    Params:
        task_id (str): The Celery task's ID.
        app (Celery): An initialized Celery app.

    Returns:
        (AsyncResult): Returns a Celery `AsyncResult` object, if task is found.
        (None): If no task is found or an exception occurs.

    """
    assert task_id, ValueError("Missing a Celery task_id")
    task_id: str = f"{task_id}"

    log.info(f"Checking Celery task '{task_id}'")
    print(f"Checking Celery task '{task_id}'")
    try:
        task_res: AsyncResult = app.AsyncResult(task_id)

        return task_res
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception getting task by ID '{task_id}'. Details: {exc}"
        )
        log.error(msg)

        return None
