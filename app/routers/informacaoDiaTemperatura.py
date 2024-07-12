import logging

from fastapi import APIRouter, HTTPException

from app.models.informacaoDiaTemperatura import InformacaoDiaTemperatura 
# from app.schemas.informacaoDiaTemperatura import InformacaoDiaTemperatura 
from app.repository.Repository import InfoRepository
from app.models.response import Response
from app.services.informacaoDiaTemperatura import InfoService

tag = 'info_dia_temp'
router = APIRouter(prefix=f'/{tag}', tags=[tag])

repository = InfoRepository()
service = InfoService()
@router.get("", response_model=list[InformacaoDiaTemperatura], name='Retornar Todos')
async def retornarTodos():
    logging.info("Retornar todos")
    return service.retornarTodos()

@router.get("/{id_dia}", response_model=InformacaoDiaTemperatura, name='Retornar por Id dia')
async def retornar_por_id_dia(id_dia: int):
    logging.info(f"Filtrar por dia: {id_dia}")
    return repository.retornarPorIdDia(id_dia)

@router.get("/{id_dia}/{x_dias}", response_model=InformacaoDiaTemperatura, name='Filtrar por Id dia e X dias')
async def retornar_por_id_dia(id_dia: int):
    return repository.retornarPorIdDia(id_dia)

@router.post("", name='Inserir multiplos registros de info')
async def salvarInfos(infos: list[InformacaoDiaTemperatura]):
    try:
        logging.info("Salvando infos")
        service.salvarInfos(infos)
    except Exception as e:
        logging.error( e)
        raise HTTPException(status_code=400, detail=str(e))
    
    return Response(sucesso=True, descricao='Sucesso')
