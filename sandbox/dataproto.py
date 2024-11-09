from loguru import logger as log
import sys

import json
import pandas as pd

from auto_weather.core import setup
from auto_weather.core.depends import db_depends
from auto_weather import weatherapi_client, datalab
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


def main():
    engine = db_depends.get_db_engine()

    current_weather_df = datalab.df_utils.load_table_into_df(
        table_name="weatherapi_current_weather", engine=engine
    )
    if isinstance(current_weather_df, pd.DataFrame):
        log.info(f"Current weather dataframe count: {current_weather_df.shape[0]}")
        log.debug(f"Current weather:\n{current_weather_df.head(5)}")


if __name__ == "__main__":
    setup.setup_loguru_logging(log_level="DEBUG")
    main()
