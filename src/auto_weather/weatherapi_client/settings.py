from __future__ import annotations

from dataclasses import dataclass, field

from dynaconf import Dynaconf
from loguru import logger as log

WEATHERAPI_SETTINGS = Dynaconf(
    environments=True,
    env="weatherapi",
    envvar_prefix="WEATHERAPI",
    settings_files=["settings.toml", ".secrets.toml"],
)


@dataclass
class WeatherAPISettings:
    location: str = field(default=None)
    api_key: str = field(default=None, repr=False)


try:
    weatherapi_settings: WeatherAPISettings = WeatherAPISettings(
        location=WEATHERAPI_SETTINGS.get("WEATHERAPI_LOCATION_NAME", default=""),
        api_key=WEATHERAPI_SETTINGS.get("WEATHERAPI_API_KEY", default=""),
    )
except Exception as exc:
    msg = f"({type(exc)}) Error initializing WeatherAPI settings. Details: {exc}"
    log.warning(msg)

    weatherapi_settings: WeatherAPISettings = WeatherAPISettings()
