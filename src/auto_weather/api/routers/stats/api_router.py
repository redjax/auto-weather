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

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/count/weather/current")
def return_current_weather_count():
    try:
        current_weather_count = weatherapi_client.client.current.get_current_weather_count()
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder({"current_weather_count": current_weather_count}))
    except Exception as exc:
        log.error(exc)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Internal server error while requesting current weather count."})
    
@router.get("/count/weather/forecast")
def return_weather_forecast_count():
    try:
        weather_forecast_count = weatherapi_client.client.forecast.get_weather_forecast_count()
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder({"weather_forecast_count": weather_forecast_count}))
    except Exception as exc:
        log.error(exc)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Internal server error while requesting weather forecast count."})