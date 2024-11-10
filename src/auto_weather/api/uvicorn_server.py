from __future__ import annotations

import typing as t
import logging

from auto_weather.api.settings import UVICORN_SETTINGS
from auto_weather.core import setup

from dynaconf import Dynaconf
from loguru import logger as log
import uvicorn
import uvicorn.config


def run_server(host: str = "127.0.0.1", port: int = 8000, reload: bool = False, log_level: str = "info", uvicorn_log_fmt: str = "%(asctime)s - %(levelname)s - %(message)s", reload_dirs: str = ["src", "/project/src"], reload_exclude_paths: list[str] = ["**/logs", "**/temp", "**/backup", "**/*.log"]):
    # log_config = uvicorn.config.LOGGING_CONFIG
    # log_config["formatters"]["access"]["fmt"] = uvicorn_log_fmt
    # log_config["formatters"]["default"]["fmt"] = uvicorn_log_fmt
    
    log.info(f"Starting Uvicorn server on port {port}")
    try:
        uvicorn.run("auto_weather.api.api_main:api_app", host=host, port=port, reload=reload, log_level=log_level, reload_excludes=reload_exclude_paths, reload_dirs=reload_dirs) # , log_config=log_config)
        log.debug(f"Uvicorn startup success")
    except Exception as exc:
        msg = f"({type(exc)}) Error running Uvicorn server. Details: {exc}"
        log.error(msg)
        
        raise exc

if __name__ == "__main__":
    setup.setup_loguru_logging()
    setup.setup_uvicorn_logging()
    # setup.add_loguru_file_handler("./logs/app.log", level="DEBUG")
    # setup.add_loguru_file_handler("./logs/error.log", level="ERROR")
    # setup.add_loguru_file_handler("./logs/access.log", level="DEBUG")
    # setup.add_loguru_file_handler("./logs/celery.log", level="DEBUG")
    # setup.add_loguru_file_handler("./logs/celery.error.log", level="ERROR")
    
    print(f"Uvicorn settings: {UVICORN_SETTINGS.as_dict()}")
    
    host=UVICORN_SETTINGS.get("UVICORN_HOST", default="127.0.0.1")
    port=UVICORN_SETTINGS.get("UVICORN_PORT", default=8000)
    reload=UVICORN_SETTINGS.get("UVICORN_RELOAD", default=False)
    log_level=UVICORN_SETTINGS.get("UVICORN_LOG_LEVEL", default="info")
    
    run_server(host=host, port=port, reload=reload, log_level=log_level)