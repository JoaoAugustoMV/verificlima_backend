from datetime import datetime
import time
from typing import List
import os, urllib, logging
logging.basicConfig(level=logging.DEBUG)
import pyodbc

from app.utils.SingletonMeta import SingletonMeta

# pyodbc.pooling = False

from sqlalchemy import create_engine, insert, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
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
            # TODO add aioodbc to requirements
            connect_str = 'mssql+aioodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_string)

            try:
                engine = create_async_engine(connect_str, pool_recycle=1500, pool_pre_ping=True)
                                
                session = async_sessionmaker(engine, expire_on_commit=False)
                print('type(session)', type(session))
                return session
            
            except Exception as e:
                attempt += 1
                if attempt <= max_attempts:
                    logging.error(f"{attempt} Try: Could not make the connection with the db", e)
                    logging.info(f"Waiting {SECONDS_TO_WAIT} seconds for server goes up")
                    time.sleep(SECONDS_TO_WAIT)
                    logging.info(f"Try new connection")   
                                    
    
        logging.error(f"Fail to connect after {attempt} attempts", e)
        raise e
                    
    async def get_all(self):
        async with self.session() as session:
            stmt = select(InformacaoDiaTemperatura)
            new_var = await session.execute(stmt)
            return new_var.scalars().all()
    
    def get_by_id_and_x_dias(self, id_dia, x_dias):
        stmt = select(InformacaoDiaTemperatura).where(InformacaoDiaTemperatura.id_dia == id_dia).where(InformacaoDiaTemperatura.x_dias == x_dias)
        return self.session.execute(stmt).first()
    
    def get_by_id_dia(self, id_dia):
        stmt = select(InformacaoDiaTemperatura).where(InformacaoDiaTemperatura.id_dia == id_dia)
        return self.session.execute(stmt).first()
    
    async def get_by_cd_dia(self, cd_dia: int) -> List[InformacaoDiaTemperatura]:        
        stmt = select(InformacaoDiaTemperatura).where(InformacaoDiaTemperatura.cd_dia == cd_dia)
        async with self.session() as session:
            current = datetime.now()
            print(cd_dia, 'start')
            resp = await session.execute(stmt)            
            print(cd_dia, 'end')
            end = datetime.now()
            diff = end - current
            print(cd_dia, diff.seconds)
            return resp.scalars().all()
    
    def insert_info(self, info: InformacaoDiaTemperatura):
        self.session.add(info)    
        return  self.session.commit()
    
    def insert_infos(self, infos: list[InformacaoDiaTemperatura]):
        self.session.add_all(infos)
        return self.session.commit()

    def update_by_id_day(self):
        pass



