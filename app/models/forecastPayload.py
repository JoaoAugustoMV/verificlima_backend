from typing import List
from pydantic import BaseModel

from app.models.dayForecast import DayForecast


class ForecastPayload(BaseModel):
    madeIn: str
    daysForecasts: List[DayForecast]