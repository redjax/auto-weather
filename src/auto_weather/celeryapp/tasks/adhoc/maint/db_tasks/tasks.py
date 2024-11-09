from __future__ import annotations

import datetime
import os
from pathlib import Path
import subprocess

from auto_weather.core.db.settings import DB_SETTINGS
from auto_weather.core.depends import db_depends

from celery import shared_task
from loguru import logger as log
import sqlalchemy as sa
