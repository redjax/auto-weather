from auto_weather.core.depends import db_depends
from auto_weather.core import db


def setup_database():
    engine = db_depends.get_db_engine()
    db.create_base_metadata(base=db.Base, engine=engine)
