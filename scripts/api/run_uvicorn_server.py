from auto_weather.api.settings import UVICORN_SETTINGS, FASTAPI_SETTINGS
from auto_weather.core.settings import LOGGING_SETTINGS
from auto_weather.core import setup
from auto_weather.api import uvicorn_server

from loguru import logger as log

if __name__== "__main__":
    setup.setup_loguru_logging(log_level=LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"), add_error_file_logger=True, add_file_logger=True)
    setup.setup_uvicorn_logging()
    setup.add_loguru_file_handler("./logs/access.log", level="DEBUG")
    
    try:
        uvicorn_server.run_server(
            host=UVICORN_SETTINGS.get("UVICORN_HOST", default="127.0.0.1"),
            port=UVICORN_SETTINGS.get("UVICORN_PORT", default=8000),
            reload=UVICORN_SETTINGS.get("UVICORN_RELOAD", default=False),
            log_level=UVICORN_SETTINGS.get("UVICORN_LOG_LEVEL", default="info"),
        )
    except Exception as exc:
        msg = f"({type(exc)}) Error running Uvicorn server. Details: {exc}"
        log.error(msg)
        
        raise exc
