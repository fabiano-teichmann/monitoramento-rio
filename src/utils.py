import pendulum


def convert_to_datetime(dt) -> pendulum.datetime:
    return pendulum.parse(dt)


def convert_to_float(value) -> float:
    return round(float(value), 2)


def get_condition(level: float, conditions: dict):
    level = int(level)
    cond = ""
    for c in conditions:
        if level >= c["nivel"]:
            cond = c["condicao"]
    return cond
