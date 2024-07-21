from pydantic import BaseModel


class ForecastSource(BaseModel):
    name: str
    urlSite: str 
    minTemperature: int
    maxTemperature: int