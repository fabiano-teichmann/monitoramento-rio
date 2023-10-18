import os

import pandas as pd
import pendulum
from sqlalchemy import create_engine
from loguru import logger

from src.settings import DATABASE_URL

engine = create_engine(DATABASE_URL)


def convert_to_datetime(dt) -> pendulum.datetime:
    return pendulum.parse(dt)


def convert_to_float(value) -> float:
    return round(float(value), 2)


def convert_string_to_float(value):
    return round(float(value.replace(",", ".")), 2)


def get_condition(level: float, conditions: dict):
    level = int(level)
    cond = "normal"
    for c in conditions:
        if level >= c["nivel"]:
            cond = c["condicao"]
    return cond


def save_status_etl(status: str, task: str, error: str = ""):
    data = [
        {
            "status": status,
            "datetime": pendulum.now(tz="America/Sao_Paulo").format('YYYY-MM-DD HH:mm'),
            "task": task,
            "error": error,
        }
    ]
    df = pd.DataFrame(data=data)
    df.to_sql("status_etl", engine, if_exists="append")


def remove_older_files():
    dt = pendulum.now().subtract(days=7)
    logger.info(
        f"Removing older files than the day {dt.format('dddd DD MMMM YYYY hh:mm')}"
    )
    path_base = os.path.join(os.getcwd(), "data")
    files = [os.path.join(path_base, f) for f in os.listdir(path_base)]
    count = 0
    for f in files:
        if pendulum.from_timestamp(os.path.getmtime(f)) < dt:
            os.remove(f)
            count += 1
    logger.info(f"Total files removed {count}")
