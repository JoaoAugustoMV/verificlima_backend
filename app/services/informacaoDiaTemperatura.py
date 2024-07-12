# from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from app.repository.Repository import InfoRepository
from app.models.informacaoDiaTemperatura import InformacaoDiaTemperatura

repository = InfoRepository()

class InfoService():

    def retornarTodos(self):
        return repository.retornarTodos()
    
    def salvarInfos(self, infos: list[InformacaoDiaTemperatura]):
        return repository.inserirInfos(infos)
