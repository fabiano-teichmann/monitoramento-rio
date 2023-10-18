import pandas as pd
from sqlalchemy import create_engine, text

from src.settings import DATABASE_URL
from src.utils import convert_to_datetime, convert_string_to_float

engine = create_engine(DATABASE_URL, echo=False)


def load_data(path: str):
    df = pd.read_csv(path, sep=";")
    df["datahora"] = df.datahora.apply(convert_to_datetime)
    df["valorMedida"] = df.valorMedida.apply(convert_string_to_float)
    dt = df.datahora[0]
    estado_ano_mes = f"{df.uf[0]}-{dt.year}-{dt.month}"
    df["estado_ano_mes"] = estado_ano_mes
    drop_old_records(estado_ano_mes)
    df.to_sql("rain_volume", engine, if_exists="replace", index=False)


def drop_old_records(estado_ano_mes: str):
    try:
        query = f"delete from rain_volume where estado_ano_mes = '{estado_ano_mes}'"
        con = engine.connect()
        con.execute(text(query))
        print(query)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    load_data(path="data/dados-pluviometricos.csv")
