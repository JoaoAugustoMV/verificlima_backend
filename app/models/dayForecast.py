from pydantic import BaseModel

from app.models.forecastSource import ForecastSource


class DayForecast(BaseModel):
    day_forecasted: str
    forecast_made_in: str
    forecast_sources: list[ForecastSource] 