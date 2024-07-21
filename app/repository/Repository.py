import time
from typing import List
import os, urllib, logging
logging.basicConfig(level=logging.DEBUG)
import pyodbc

from app.utils.SingletonMeta import SingletonMeta

pyodbc.pooling = False

from sqlalchemy import create_engine, insert, select
from sqlalchemy.orm import Session
from sqlmodel import SQLModel

from app.models.informacaoDiaTemperatura import InformacaoDiaTemperatura

SECONDS_TO_WAIT = 10
class InfoRepository(metaclass=SingletonMeta):

    def __init__(self):
        self.session = self.get_session()

    def get_session(self, max_attempts=3, attempt=0):
        while attempt < max_attempts:
            odbc_string = os.getenv('stringConnectionAzure')
            connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_string)

            try:
                engine = create_engine(connect_str, connect_args={"check_same_thread": False}, pool_recycle=1500)
                SQLModel.metadata.create_all(engine)

                conn = engine.connect()
                return Session(conn)
            
            except Exception as e:
                if attempt <= max_attempts:
                    logging.error(f"{attempt} Try: Could not make the connection with the db", e)
                    logging.info(f"Waiting {SECONDS_TO_WAIT} seconds for server goes up")
                    time.sleep(SECONDS_TO_WAIT)
                    logging.info(f"Try new connection")                    
    
        logging.error(f"Fail to connect after {attempt} attempts", e)
        raise e
                    

    def retornarTodos(self):
        return self.session.query(InformacaoDiaTemperatura).all()        
    
    def retornarPorIdDiaEXDias(self, id_dia, x_dias):
        stmt = select(InformacaoDiaTemperatura).where(InformacaoDiaTemperatura.id_dia == id_dia).where(InformacaoDiaTemperatura.x_dias == x_dias)
        return self.session.execute(stmt).first()
    
    def retornarPorIdDia(self, id_dia):
        stmt = select(InformacaoDiaTemperatura).where(InformacaoDiaTemperatura.id_dia == id_dia)
        return self.session.execute(stmt).first()
    
    def retornarPorCdDia(self, cd_dia: int) -> List[InformacaoDiaTemperatura]:
        # stmt = select(InformacaoDiaTemperatura).where(InformacaoDiaTemperatura.cd_dia == cd_dia)
        return self.session.query(InformacaoDiaTemperatura).filter(InformacaoDiaTemperatura.cd_dia == cd_dia)
        return self.session.execute(stmt)
    
    def inserirInfo(self, info: InformacaoDiaTemperatura):
        self.session.add(info)    
        return  self.session.commit()
    
    def inserirInfos(self, infos: list[InformacaoDiaTemperatura]):
        self.session.add_all(infos)
        return self.session.commit()

    def updateByIdDay(self):
        pass



