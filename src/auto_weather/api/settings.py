from __future__ import annotations

import typing as t

from dynaconf import Dynaconf
from loguru import logger as log

FASTAPI_SETTINGS = Dynaconf(environments=True, env="fastapi", envvar_prefix="FASTAPI", settings_files=["settings.toml", ".secrets.toml"])
UVICORN_SETTINGS = Dynaconf(environments=True, env="uvicorn", envvar_prefix="UVICORN", settings_files=["settings.toml", ".secrets.toml"])