from __future__ import annotations

import typing as t

from fastapi import FastAPI
from loguru import logger as log

api_app = FastAPI()

@api_app.get("/")
def read_root():
    return {"msg": "Hello, world!"}
