from __future__ import annotations

from loguru import logger as log
import time
import typing as t

from celery.result import AsyncResult
from auto_weather.celeryapp.celery_main import celery_app, check_task
from auto_weather.celeryapp.settings import CELERY_SETTINGS
from auto_weather.celeryapp.tasks.adhoc.weather.weatherapi_tasks import (
    task_weatherapi_current_weather,
)
from auto_weather.core.setup import setup_database, setup_loguru_logging
from auto_weather.weatherapi_client.settings import WEATHERAPI_SETTINGS


def run(task_check_sleep: int = 5, location_name: str = None):
    # task_result: AsyncResult = task_count_current_weather_rows.delay()
    task_result: AsyncResult = celery_app.send_task("weatherapi-weather-forecast")

    while not check_task(task_id=task_result.task_id, app=celery_app).ready():
        log.info(f"Task {task_result.task_id} is in state [{task_result.state}]")

        if task_result.state == "FAILURE":
            log.error(f"Error executing task {task_result.id}.")

            return None

        if task_check_sleep:
            log.info(f"Sleeping for [{task_check_sleep}] second(s)...")
            time.sleep(task_check_sleep)

    ## Task is ready
    log.info(
        f"Task {task_result.task_id} ready=True. State: {check_task(task_id=task_result.task_id, app=celery_app).state}"
    )

    log.info("Finish getting weather forecast")

    if task_result.result is None:
        log.warning("Result is None, an error may have occurred")

        return None
    else:
        if task_result and task_result.result:
            log.debug(f"Results: {task_result.result}")
            log.debug(f"task_result.result type: ({type(task_result.result)})")

            return task_result.result
        else:
            log.warning(
                "Task's result field is None. This could indicate an error, but may be normal operation."
            )


def main(task_check_sleep: int = 5):
    weather_forecast = run(task_check_sleep=task_check_sleep)
    if weather_forecast is None:
        log.warning("weather_forecast object is None, an error may have occurred")
    else:
        log.info(f"Weather forecast result: {weather_forecast}")


if __name__ == "__main__":
    setup_loguru_logging(log_level="DEBUG")

    main(task_check_sleep=2)
