import typing as t

from loguru import logger as log

from dynaconf import Dynaconf

FASTAPI_SETTINGS = Dynaconf(environments=True, env="fastapi", envvar_prefix="FASTAPI", settings_files=["settings.toml", ".secrets.toml"])
UVICORN_SETTINGS = Dynaconf(environments=True, env="uvicorn", envvar_prefix="UVICORN", settings_files=["settings.toml", ".secrets.toml"])