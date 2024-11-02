from loguru import logger as log
import sys

from auto_weather import weatherapi_client

log.remove(0)
log.add(
    sys.stderr,
    format="{time:YYYY-MM-DD HH:mm:ss} | [{level}] | ({module}.{function}:{line}) | > {message}",
    level="DEBUG",
)
log.enable("auto_weather")


def main():
    log.info("Prototype start")

    current_weather = weatherapi_client.client.current.get_current_weather()
    log.info(f"Current weather ({type(current_weather)}): {current_weather}")


if __name__ == "__main__":
    main()
