from __future__ import annotations

from auto_weather import domain, weatherapi_client
from auto_weather.celeryapp.celery_main import celery_app
from auto_weather.core.depends.db_depends import get_session_pool
from auto_weather.domain import (
    CurrentWeatherIn,
    CurrentWeatherModel,
    CurrentWeatherOut,
    CurrentWeatherRepository,
    LocationIn,
    LocationModel,
    LocationOut,
    LocationRepository,
)
from auto_weather.weatherapi_client.settings import weatherapi_settings

from loguru import logger as log

@log.catch
@celery_app.task(name="weatherapi-current-weather")
def task_weatherapi_current_weather(
    use_cache: bool = False,
    api_key: str = weatherapi_settings.api_key,
    location: str = weatherapi_settings.location,
):
    """Request & save current weather from WeatherAPI."""
    print(f"API key: {api_key}, location: {location}")

    try:
        current_weather_res = weatherapi_client.client.current.get_current_weather(
            api_key=api_key, location=location, use_cache=use_cache
        )
        log.debug(
            f"Current weather ({type(current_weather_res)}): {current_weather_res}"
        )
        print(
            f"[TEMP] Current weather ({type(current_weather_res)}): {current_weather_res}"
        )
    except Exception as exc:
        log.error(
            f"({type(exc)}) Error requesting current weather from WeatherAPI. Details: {exc}"
        )

        raise

    location: LocationIn = weatherapi_client.convert.location_dict_to_schema(
        current_weather_res["location"]
    )
    log.debug(f"Location: {location}")

    current_weather: CurrentWeatherIn = (
        weatherapi_client.convert.current_weather_dict_to_schema(
            current_weather_res["current"]
        )
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

    return_obj: dict = {
        "current_weather": current_weather.model_dump(),
        "location": location.model_dump(),
    }

    log.info(f"Finish Celery task requesting current weather from WeatherAPI")

    return return_obj


@log.catch
@celery_app.task(name="weatherapi-weather-forecast")
def task_weather_forecast(
    use_cache: bool = False, location: str = weatherapi_settings.location
) -> dict[str, domain.weather.forecast.ForecastJSONOut]:
    if location is None:
        log.warning(
            "No location detected. Set a WEATHERAPI_LOCATION_NAME environnment variable with a value of a location to search weatherAPI for."
        )

        return None

    log.info("Getting weather forecast in background")

    try:
        weather_forecast_res: dict = weatherapi_client.client.get_weather_forecast(
            use_cache=use_cache, location=location
        )
    except Exception as exc:
        msg = f"({type(exc)}) Error running background task to get weather forecast. Details: {exc}"
        log.error(msg)

        raise exc

    if weather_forecast_res:
        weather_forecast: domain.weather.forecast.ForecastJSONIn = (
            domain.weather.forecast.ForecastJSONIn(
                forecast_json=weather_forecast_res["forecast"]
            )
        )
        log.info(f"Weather forecast: {weather_forecast}")
        return {"weather_forecast": weather_forecast.model_dump()}
    else:
        log.warning("Weather forecast object is None. An error may have occurred.")
        return {"weather_forecast": None}


@log.catch
@celery_app.task(name="weatherapi-current-weather-count")
def task_count_current_weather_rows():
    session_pool = get_session_pool()

    with session_pool() as session:
        repo = domain.CurrentWeatherRepository(session=session)

        rows = repo.count()

    log.info(f"Found [{rows}] row(s) in the current weather table")

    return {"count": rows}


@log.catch
@celery_app.task(name="weatherapi-forecast-count")
def task_count_weather_forecast_rows():
    session_pool = get_session_pool()

    with session_pool() as session:
        repo = domain.ForecastJSONRepository(session=session)

        rows = repo.count()

    log.info(f"Found [{rows}] row(s) in the weather forecast table")

    return {"count": rows}
