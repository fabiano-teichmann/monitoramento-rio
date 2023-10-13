from rocketry import Rocketry
import pendulum
from loguru import logger
from rocketry.conditions.api import cron

from src.river_level import RiverLevel

app = Rocketry()


@app.task(cron("10 * * * *"))
def extract_level_river():
    logger.info("Start extraction")
    RiverLevel().execute()
    now = pendulum.now(tz="America/Sao_Paulo").format("dddd DD MMMM YYYY HH:mm")
    logger.info(f"Finished extraction {now}")


if __name__ == "__main__":
    app.run()
