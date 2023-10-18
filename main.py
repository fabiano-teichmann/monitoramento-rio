from rocketry import Rocketry
import pendulum
from loguru import logger
from rocketry.conditions.api import cron, daily

from src.river_level import RiverLevel
from src.utils import save_status_etl, remove_older_files

app = Rocketry()


@app.task(cron("10 * * * *"))
def extract_level_river():
    try:
        logger.info("Start extraction")
        RiverLevel().execute()
        now = pendulum.now(tz="America/Sao_Paulo").format("dddd DD MMMM YYYY HH:mm")
        logger.info(f"Finished extraction {now}")
        save_status_etl(status="success", task="river_level")
    except Exception as e:
        logger.error(e)
        save_status_etl(status="error", task="river_level", error=str(e))


@app.task(daily)
def task_remove_older_files():
    remove_older_files()


if __name__ == "__main__":
    RiverLevel().execute()
    app.run()
