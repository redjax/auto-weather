from __future__ import annotations

from auto_weather.celeryapp.tasks.scheduled.demo import TASK_SCHEDULE_1m_say_hello

from .settings import BACKEND_URL, BROKER_URL, CELERY_SETTINGS

from celery import Celery, current_app
from celery.result import AsyncResult

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
    ## Configure celery beat schedule
    celery_app.conf.beat_schedule = {
        **TASK_SCHEDULE_1m_say_hello,
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

    # log.info(f"Checking Celery task '{task_id}'")
    print(f"Checking Celery task '{task_id}'")
    try:
        task_res: AsyncResult = app.AsyncResult(task_id)

        return task_res
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception getting task by ID '{task_id}'. Details: {exc}"
        )
        # log.error(msg)
        print(f"[ERROR] {msg}")

        return None


@celery_app.task
def add(x, y):
    return x + y


@celery_app.task
def tsum(*args, **kwargs):
    print(args)
    print(kwargs)
    return sum(args[0])
