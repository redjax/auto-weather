from __future__ import annotations

import typing as t

from auto_weather import weatherapi_client
from auto_weather.domain import (
    CurrentWeatherIn,
    CurrentWeatherModel,
    CurrentWeatherOut,
)
from auto_weather.domain import ForecastJSONIn, ForecastJSONModel, ForecastJSONOut

from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from loguru import logger as log

router = APIRouter(prefix="/weather", tags=["weather"])

# @router.get("/")
# def weather_api_root():
#     return {"msg": "Weather route reached"}


@router.get("/current")
def return_current_weather():
    try:
        current_weather_res = weatherapi_client.client.current.get_current_weather()
    except Exception as exc:
        log.error(exc)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Internal server error while requesting current weather."})

    if current_weather_res is None:
        log.warning("Current weather response is None")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Internal server error while requesting current weather, response should not have been None."})

    current_weather = CurrentWeatherIn.model_validate(current_weather_res["current"])
    
    try:
        res = jsonable_encoder(current_weather.model_dump())
        return JSONResponse(status_code=status.HTTP_200_OK, content=res)
    
    except Exception as exc:
        log.error(exc)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Internal server error while converting current weather response to JSON."})


@router.get("/forecast")
def return_weather_forecast():
    try:
        weather_forecast_res = weatherapi_client.client.forecast.get_weather_forecast()
    except Exception as exc:
        log.error(exc)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Internal server error while requesting weather forecast."})

    if weather_forecast_res is None:
        log.warning("Weather forecast response is None")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Internal server error while requesting weather forecast, response should not have been None."})

    weather_forecast = ForecastJSONIn(forecast_json=weather_forecast_res)
    
    try:
        res = jsonable_encoder(weather_forecast.forecast_json)
        return JSONResponse(status_code=status.HTTP_200_OK, content=res)
    
    except Exception as exc:
        log.error(exc)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Internal server error while converting weather forecast response to JSON."})
