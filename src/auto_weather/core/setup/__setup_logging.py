from __future__ import annotations

import sys
import logging
from loguru import logger
from uvicorn import Config, Server
from auto_weather.core.settings import LOGGING_SETTINGS

LOG_LEVEL = LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO")
_ts: str = "[{time:YYYY-MM-DD_HH:mm:ss}]"
_level: str = "[{level}]"
_name_line: str = "[{name}:{line}]"
_msg: str = "{message}"
default_color_fmt: str = (
    f"<green>{_ts}</green> <level>{_level}</level> > <level>{_name_line}</level>: {_msg}"
)

class InterceptHandler(logging.Handler):
    def emit(self, record):
        # get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # find caller from where originated the logged message
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_uvicorn_logging(
    colorize: bool = True, fmt: str = default_color_fmt, level: str = LOG_LEVEL
):
    logger.configure(
        handlers=[
            {
                "sink": sys.stderr,
                "format": fmt,
                "colorize": colorize,
                "level": level,
            }
        ]
    )

    intercept_handler = InterceptHandler()

    # level=NOTSET - loguru controls actual level
    logging.basicConfig(handlers=[intercept_handler], level=logging.NOTSET)

    for name in logging.root.manager.loggerDict.keys():
        _logger = logging.getLogger(name)
        if _logger.name.startswith("gunicorn"):
            _logger.handlers = [intercept_handler]
        else:
            # By default uvicorn.access has a handler and doesn't propagate
            # (uvicorn.access controls INFO messages on requests)
            _logger.propagate = True
            _logger.handlers = []

def setup_loguru_logging(
    log_level: str = "INFO",
    enable_loggers: list[str] = ["auto_weather"],
    add_file_logger: bool = False,
    add_error_file_logger: bool = False,
):
    logger.remove(0)
    logger.add(
        sys.stderr,
        format="{time:YYYY-MM-DD HH:mm:ss} | [{level}] | ({module}.{function}:{line}) | > {message}",
        level=log_level,
    )

    if enable_loggers:
        for _logger in enable_loggers:
            logger.enable(_logger)

    if add_file_logger:
        logger.add("logs/app.log", retention=3, rotation="15 MB", level="DEBUG")

    if add_error_file_logger:
        logger.add("logs/error.log", retention=3, rotation="15 MB", level="ERROR")


def add_loguru_file_handler(log_file: str = "logs/app.log", level: str ="INFO", rotation: str ="10 MB", compression: str ="zip", enqueue: bool =True):
    logger.add(log_file, level=level, rotation=rotation, compression=compression, enqueue=enqueue)
