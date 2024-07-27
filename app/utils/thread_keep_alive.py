import time
import logging
from threading import Thread
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.repository.Repository import InfoRepository

repository = InfoRepository()   
def query_keep_alive():

    while True:
        time.sleep(900)
        try:
            logging.info("Try  to ping - keep alive")
            repository.session.execute(text('SELECT 1'))
            logging.info("Keep alive finished")
        except Exception as e:
            logging.error("Error - Keep Alive", e)
            break

def keep_connection_alive():
    keep_alive_thread = Thread(target=query_keep_alive)
    keep_alive_thread.daemon = True
    keep_alive_thread.start()