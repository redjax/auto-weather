from os import environ
from celery import Celery

environ.setdefault("CELERY_CONFIG_MODULE", "auto_weather.celeryapp.celery_config")

app = Celery()
app.config_from_envvar("CELERY_CONFIG_MODULE")


@app.task
def add(x, y):
    return x + y


@app.task
def tsum(*args, **kwargs):
    print(args)
    print(kwargs)
    return sum(args[0])
