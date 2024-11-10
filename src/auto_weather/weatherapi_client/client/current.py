from __future__ import annotations

import time

from auto_weather.core import http_lib
from auto_weather.core.depends import db_depends
from auto_weather.weatherapi_client.settings import weatherapi_settings
from auto_weather.domain import CurrentWeatherRepository

from . import requests

import httpx
from loguru import logger as log

def get_current_weather(
    location: str = weatherapi_settings.location,
    api_key: str = weatherapi_settings.api_key,
    include_aqi: bool = True,
    headers: dict | None = None,
    use_cache: bool = False,
    retry: bool = True,
    max_retries: int = 3,
    retry_sleep: int = 5,
    retry_stagger: int = 3,
    save_to_db: bool = True,
):
    current_weather_request: httpx.Request = requests.return_current_weather_request(
        api_key=api_key, location=location, include_aqi=include_aqi, headers=headers
    )

    log.info("Requesting current weather")

    with http_lib.get_http_controller(use_cache=use_cache) as http:
        try:
            res: httpx.Response = http.client.send(current_weather_request)
        except httpx.ReadTimeout as timeout:
            log.warning(
                f"({type(timeout)}) Operation timed out while requesting current weather."
            )

            if not retry:
                raise timeout
            else:
                log.info(f"Retrying {max_retries} time(s)")
                current_attempt = 0
                _sleep = retry_sleep

                while current_attempt < max_retries:
                    if current_attempt > 0:
                        _sleep += retry_stagger

                    log.info(f"[Retry {current_attempt}/{max_retries}]")

                    try:
                        res: httpx.Response = http.client.send(current_weather_request)
                        break
                    except httpx.ReadTimeout as timeout_2:
                        log.warning(
                            f"ReadTimeout on attempt [{current_attempt}/{max_retries}]"
                        )

                        current_attempt += 1

                        time.sleep(retry_sleep)

                        continue

    log.debug(f"Response: [{res.status_code}: {res.reason_phrase}]")

    if save_to_db:
        log.warning("Saving current weather to database is not implemented")

    if res.status_code in http_lib.constants.SUCCESS_CODES:
        log.info("Success requesting current weather")
        decoded = http_lib.decode_response(response=res)
    elif res.status_code in http_lib.constants.ALL_ERROR_CODES:
        log.warning(f"Error: [{res.status_code}: {res.reason_phrase}]: {res.text}")

        return None
    else:
        log.error(
            f"Unhandled error code: [{res.status_code}: {res.reason_phrase}]: {res.text}"
        )

        return None

    return decoded


def get_current_weather_count() -> int:
    session_pool = db_depends.get_session_pool()
    
    try:
        with session_pool() as session:
            repo = CurrentWeatherRepository(session=session)
            
            current_weather_count = repo.count()
            return current_weather_count
    except Exception as exc:
        msg = f"({type(exc)}) Error getting current weather count. Details: {exc}"
        log.error(msg)
        
        return None
