import os
import subprocess
import datetime

from pathlib import Path

from auto_weather.core.depends import db_depends
from auto_weather.core.db.settings import DB_SETTINGS

from loguru import logger as log
from celery import shared_task
import sqlalchemy as sa
