from loguru import logger as log

from auto_weather.domain import (
    CurrentWeatherIn,
    LocationIn,
    CurrentWeatherOut,
    CurrentWeatherModel,
)


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


@log.catch
def current_weather_schema_to_model(current_weather_schema: CurrentWeatherIn):
    raise NotImplementedError(
        "Converting current weather schema to database model not yet supported."
    )
    current_weather_model: CurrentWeatherModel = CurrentWeatherModel(
        **current_weather_schema.model_dump()
    )

    return current_weather_model


@log.catch
def current_weather_model_to_schema(current_weather_model: CurrentWeatherModel):
    current_weather_schema: CurrentWeatherOut = CurrentWeatherOut.model_validate(
        current_weather_model.__dict__
    )

    return current_weather_schema
