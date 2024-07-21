from pydantic import BaseModel

from app.models.forecastSource import ForecastSource


class DayForecast(BaseModel):
    dayForecasted: str
    forecastMadeIn: str
    forecastSources: list[ForecastSource] 