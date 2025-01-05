from __future__ import annotations

from auto_weather.core.depends import db_depends

from .constants import PD_ENGINE, PQ_ENGINE

from loguru import logger as log
import pandas as pd
import sqlalchemy as sa

def load_table_into_df(
    table_name: str, engine: sa.Engine = db_depends.get_db_engine()
) -> pd.DataFrame:
    try:
        df: pd.DataFrame = pd.read_sql_table(table_name=table_name, con=engine)

        return df
    except Exception as exc:
        msg = f"({type(exc)}) Error loading table '{table_name}' into DataFrame. Details: {exc}"
        log.error(msg)

        raise exc
