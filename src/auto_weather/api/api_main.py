from __future__ import annotations

import typing as t
from contextlib import asynccontextmanager
import logging

from auto_weather.api.settings import FASTAPI_SETTINGS

from .routers import api_router

from fastapi import FastAPI
from loguru import logger as log

api_app = FastAPI(debug=FASTAPI_SETTINGS.get("FASTAPI_DEBUG", default=False), title=FASTAPI_SETTINGS.get("FASTAPI_TITLE", default="auto-weather API"), summary=FASTAPI_SETTINGS.get("FASTAPI_SUMMARY", default=""), description=FASTAPI_SETTINGS.get("FASTAPI_DESCRIPTION", default=""), version=FASTAPI_SETTINGS.get("FASTAPI_VERSION", default="0.0.1"))
api_app.include_router(api_router.router)


@api_app.get("/")
def read_root():
    return {"msg": "Hello, world!"}
