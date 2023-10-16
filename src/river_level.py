import os
import json
from typing import List

import pendulum
from loguru import logger
import httpx
import pandas as pd
from sqlalchemy import create_engine

from src.settings import ALERTBU_BASE_URL, DATABASE_URL
from src.utils import get_condition, convert_to_datetime

engine = create_engine(DATABASE_URL)


class RiverLevel:
    def __init__(self):
        self.url = os.path.join(ALERTBU_BASE_URL, "static/data/nivel_oficial.json")
        now = pendulum.now(tz="America/Sao_Paulo").isoformat()
        self.path_level = os.path.join(os.getcwd(), "data", f"level-{now}.json")

    def __get_data(self):
        logger.info("Get level river")
        resp = httpx.get(self.url, verify=False)
        resp.raise_for_status()
        return resp.json()

    def __extract(self):
        logger.info(f"Save data in {self.path_level}")
        data = self.__get_data()
        with open(self.path_level, "w") as f:
            json.dump(data, f)

    def __build_data(self, data, conditions: dict) -> List[dict]:
        payload = []
        last_dt, last_level = self.__get_historical()
        for d in data:
            last_level = payload[-1]["nivel"] if payload else last_level
            dt = convert_to_datetime(d["horaLeitura"])
            if dt > last_dt:
                payload.append(
                    {
                        "data_hora_leitura": dt,
                        "nivel": round(d["nivel"], 2),
                        "variacao": round(d["nivel"] - last_level, 2),
                        "rio": "itajai-içu",
                        "condicao": get_condition(d["nivel"], conditions),
                    }
                )
        return payload

    @staticmethod
    def __get_historical():
        logger.info("Get historical data")
        data = pd.read_sql(
            sql="select * from level_river order by data_hora_leitura desc limit 1",
            con=engine,
        ).to_dict(orient="records")
        return data[0]["data_hora_leitura"], data[0]["nivel"]

    def __transform(self):
        logger.info("Transform data")
        payload = json.load(open(self.path_level, "r"))
        levels = payload["niveis"]
        conditions = payload["condicoes"]
        return self.__build_data(data=levels, conditions=conditions)

    def execute(self):
        self.__extract()
        level = self.__transform()
        if level:
            df = pd.DataFrame(level)
            df.to_sql("level_river", engine, if_exists="append", index=False)
            logger.info("Add new record")
        else:
            logger.info("Not has records")


if __name__ == "__main__":
    RiverLevel().execute()
