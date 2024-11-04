from __future__ import annotations

from celery import shared_task
from auto_weather.celeryapp.celery_main import celery_app

from loguru import logger as log


# @celery_app.task(name="say_hello")
@shared_task(name="say_hello")
def task_say_hello(name: str = "world"):
    log.debug(f"Name: {name}")

    print(f"Hello, {name}!")

    return {"msg": f"Said hello to: {name}"}
