import asyncio
import time
import logging
from threading import Thread
from sqlalchemy.orm import Session
from sqlalchemy import select, text

from app.repository.Repository import InfoRepository

repository = InfoRepository()   
async def query_keep_alive():

    while True:        
        time.sleep(600)
        try:
            logging.info("Try  to ping - keep alive")
            async with repository.session() as session:
                stmt = select(1)
                await session.execute(stmt)                            
            logging.info("Keep alive finished")
        except Exception as e:
            logging.error("Error - Keep Alive", e)
            break
        
def wrap_async_func():
    asyncio.run(query_keep_alive())

def keep_connection_alive():
    keep_alive_thread = Thread(target=wrap_async_func)
    keep_alive_thread.daemon = True
    keep_alive_thread.start()