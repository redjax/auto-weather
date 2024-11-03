from loguru import logger as log

from auto_weather.domain import CurrentWeatherIn, LocationIn


@log.catch
def current_weather_dict_to_schema(current_weather_dict: dict):
    current_weather: CurrentWeatherIn = CurrentWeatherIn.model_validate(
        current_weather_dict
    )

    return current_weather


@log.catch
def location_dict_to_schema(location_dict: dict):
    location: LocationIn = LocationIn.model_validate(location_dict)

    return location
