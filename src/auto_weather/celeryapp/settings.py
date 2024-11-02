from dynaconf import Dynaconf

CELERY_SETTINGS = Dynaconf(
    environments=True,
    env="celery",
    envvar_prefix="CELERY",
    settings_files=["settings.toml", ".secrets.toml"],
)


BROKER_URL = CELERY_SETTINGS.get("CELERY_BROKER_URL", default="")
BACKEND_URL = CELERY_SETTINGS.get("CELERY_BACKEND_URL", default="")
