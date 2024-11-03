import sys
from loguru import logger


def setup_loguru_logging(
    log_level: str = "INFO", enable_loggers: list[str] = ["auto_weather"]
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
