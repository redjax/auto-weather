from __future__ import annotations

import typing as t

from auto_weather.api.settings import UVICORN_SETTINGS
from auto_weather.core import setup

from dynaconf import Dynaconf
from loguru import logger as log
import uvicorn

def run_server(host: str = "127.0.0.1", port: int = 8000, reload: bool = False, log_level: str =    "info"):
    try:
        uvicorn.run("auto_weather.api.api_main:api_app", host=host, port=port, reload=reload, log_level=log_level)
    except Exception as exc:
        msg = f"({type(exc)}) Error running Uvicorn server. Details: {exc}"
        log.error(msg)
        
        raise exc

if __name__ == "__main__":
    setup.setup_loguru_logging()
    
    print(f"Uvicorn settings: {UVICORN_SETTINGS.as_dict()}")
    
    host=UVICORN_SETTINGS.get("UVICORN_HOST", default="127.0.0.1")
    port=UVICORN_SETTINGS.get("UVICORN_PORT", default=8000)
    reload=UVICORN_SETTINGS.get("UVICORN_RELOAD", default=False)
    log_level=UVICORN_SETTINGS.get("UVICORN_LOG_LEVEL", default="info")
    
    run_server(host=host, port=port, reload=reload, log_level=log_level)