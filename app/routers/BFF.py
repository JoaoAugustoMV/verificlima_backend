import logging

from fastapi import APIRouter

from app.models.forecastPayload import ForecastPayload
from app.repository.Repository import InfoRepository
from app.services.informacaoDiaTemperatura import InfoService

tag = 'bff'
router = APIRouter(prefix=f'/{tag}', tags=[tag])

repository = InfoRepository()
service = InfoService()


@router.get("/get_current_week", response_model=list[ForecastPayload], name='Get current week info')
async def get_all():
    logging.info("get_current_week")
    return service.get_current_week()