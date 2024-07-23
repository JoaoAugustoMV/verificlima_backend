from pydantic import BaseModel


class ForecastSource(BaseModel):
    name: str
    url_site: str 
    min_temperature: int
    max_temperature: int