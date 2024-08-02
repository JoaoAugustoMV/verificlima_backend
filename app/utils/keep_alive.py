import logging
import asyncio
from sqlalchemy import text
from app.repository.Repository import InfoRepository
from app.utils.configs import SECONDS_TO_KEEP_ALIVE


repository = InfoRepository()
async def keep_alive_session():
    logging.info("Starting keep alive function")
    while True:
        await asyncio.sleep(SECONDS_TO_KEEP_ALIVE)
        try:
            logging.info("Try  to ping - keep alive")
            repository.session.execute(text('SELECT 1'))
            logging.info("Keep alive finished")
        except Exception as e:
            logging.error("Error - Keep Alive", e)
            break
