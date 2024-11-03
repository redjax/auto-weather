from loguru import logger as log
import sys

import json

from auto_weather import weatherapi_client
from auto_weather.domain import (
    CurrentWeatherIn,
    CurrentWeatherOut,
    CurrentWeatherModel,
    CurrentWeatherRepository,
    LocationIn,
    LocationModel,
    LocationOut,
    LocationRepository,
)


log.remove(0)
log.add(
    sys.stderr,
    format="{time:YYYY-MM-DD HH:mm:ss} | [{level}] | ({module}.{function}:{line}) | > {message}",
    level="DEBUG",
)
log.enable("auto_weather")


def main():
    log.info("Prototype start")

    current_weather_dict = weatherapi_client.client.current.get_current_weather()
    log.debug(f"Current weather ({type(current_weather_dict)}): {current_weather_dict}")

    location = LocationIn.model_validate(current_weather_dict["location"])
    log.debug(f"Location: {location}")

    current_weather = CurrentWeatherIn.model_validate(current_weather_dict["current"])
    log.info(f"Current weather: {current_weather}")


if __name__ == "__main__":
    main()
