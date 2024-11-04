from auto_weather.celeryapp.celery_main import celery_app
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


from loguru import logger as log

from auto_weather import weatherapi_client
from auto_weather.weatherapi_client.settings import weatherapi_settings

from auto_weather.celeryapp.celery_main import celery_app
from auto_weather.core.depends.db_depends import get_session_pool
from auto_weather import domain
from auto_weather import weatherapi_client


@log.catch
@celery_app.task(name="weatherapi-current-weather")
def task_weatherapi_current_weather(
    api_key: str = weatherapi_settings.api_key,
    location: str = weatherapi_settings.location,
):
    """Request & save current weather from WeatherAPI."""
    try:
        current_weather_res = weatherapi_client.client.current.get_current_weather(
            api_key=api_key, location=location
        )
        log.debug(
            f"Current weather ({type(current_weather_res)}): {current_weather_res}"
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
@celery_app.task(name="current_weather_count")
def task_count_current_weather_rows():
    session_pool = get_session_pool()

    with session_pool() as session:
        repo = domain.CurrentWeatherRepository(session=session)

        rows = repo.count()

    log.info(f"Found [{rows}] row(s) in the current weather table")

    return {"count": rows}


@log.catch
@celery_app.task(name="weather_forecast_count")
def task_count_weather_forecast_rows():
    session_pool = get_session_pool()

    with session_pool() as session:
        repo = domain.ForecastJSONRepository(session=session)

        rows = repo.count()

    log.info(f"Found [{rows}] row(s) in the weather forecast table")

    return {"count": rows}
