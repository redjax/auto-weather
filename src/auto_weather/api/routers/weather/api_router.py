from __future__ import annotations

import typing as t

from auto_weather import weatherapi_client
from auto_weather.domain.weather.current import (
    CurrentWeatherIn,
    CurrentWeatherModel,
    CurrentWeatherOut,
)

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
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Internal server error while requesting current weather."})

    current_weather = CurrentWeatherIn.model_validate(current_weather_res["current"])
    
    try:
        res = jsonable_encoder(current_weather.model_dump())
        return JSONResponse(status_code=status.HTTP_200_OK, content=res)
    
    except Exception as exc:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Internal server error while converting current weather response to JSON."})
