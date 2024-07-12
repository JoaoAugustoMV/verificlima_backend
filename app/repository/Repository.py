import os, urllib

from sqlalchemy import create_engine, insert, select
from sqlalchemy.orm import Session
from sqlmodel import SQLModel

from app.models.informacaoDiaTemperatura import InformacaoDiaTemperatura

# Connect to the database
odbc_string = os.getenv('stringConnectionAzure')
connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_string)
engine = create_engine(connect_str)
SQLModel.metadata.create_all(engine)

conn = engine.connect()
session = Session(conn)

class InfoRepository:

    def __init__(self):
        self.session = session

    def retornarTodos(self):
        stmt = select(InformacaoDiaTemperatura)
        # teste = self.session.get()
        resul = self.session.query(InformacaoDiaTemperatura).all()
        return self.session.query(InformacaoDiaTemperatura).all()
        # return [r.InformacaoDiaTemperatura for r in self.session.execute(stmt)]
    
    def retornarPorIdDiaEXDias(self, id_dia, x_dias):
        stmt = select(InformacaoDiaTemperatura).where(InformacaoDiaTemperatura.id_dia == id_dia).where(InformacaoDiaTemperatura.x_dias == x_dias)
        return self.session.execute(stmt).first()
    
    def retornarPorIdDia(self, id_dia):
        stmt = select(InformacaoDiaTemperatura).where(InformacaoDiaTemperatura.id_dia == id_dia)
        return self.session.execute(stmt).first()
    
    def inserirInfo(self, info: InformacaoDiaTemperatura):
        self.session.add(info)    
        return  self.session.commit()
    
    def inserirInfos(self, infos: list[InformacaoDiaTemperatura]):
        self.session.add_all(infos)
        return self.session.commit()

    def updateByIdDay(self):
        pass



