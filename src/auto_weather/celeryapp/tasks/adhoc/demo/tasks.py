from auto_weather.celeryapp.celery_main import celery_app


@celery_app.task(name="say_hello")
def task_say_hello(name: str = "world"):
    print(f"Hello, {name}!")
