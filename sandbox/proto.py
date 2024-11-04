from loguru import logger as log
import sys

import json

from auto_weather.core import setup
from auto_weather import weatherapi_client
from auto_weather.domain import (
    CurrentWeatherIn,
    CurrentWeatherOut,
    CurrentWeatherModel,
    CurrentWeatherRepository,
)
from auto_weather.domain import (
    LocationIn,
    LocationModel,
    LocationOut,
    LocationRepository,
)


def demo_weatherapi_current_weather():
    current_weather_res = weatherapi_client.client.current.get_current_weather()
    log.debug(f"Current weather ({type(current_weather_res)}): {current_weather_res}")

    location = weatherapi_client.convert.location_dict_to_schema(
        current_weather_res["location"]
    )
    log.debug(f"Location: {location}")

    current_weather = weatherapi_client.convert.current_weather_dict_to_schema(
        current_weather_res["current"]
    )
    log.info(f"Current weather: {current_weather}")

    log.info("Saving current weather & location to database")
    try:
        weatherapi_client.client.db_ops.save_current_weather(
            current_weather_schema=current_weather, location_schema=location
        )
    except Exception as exc:
        msg = f"({type(exc)}) Error saving current weather & location to database. Details: {exc}"
        log.error(msg)


def main():
    log.info("Prototype start")

    demo_weatherapi_current_weather()


if __name__ == "__main__":
    setup.setup_loguru_logging(log_level="DEBUG")
    setup.setup_database()

    main()
