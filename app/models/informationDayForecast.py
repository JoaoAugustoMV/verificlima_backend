from pydantic import BaseModel, Field
from typing import Optional

class InformationDayForecast(BaseModel):
    id: str = None
    cd_dia: int
    x_dias: int = None
    dia_previsao_feita_menos_x: str = None
    temperatura_min_previsao_feita_menos_x: Optional[int] = Field(default=None)
    temperatura_max_previsao_feita_menos_x: Optional[int] = Field(default=None)
    
    temperatura_real_min: Optional[int] = Field(default=None)
    temperatura_real_max: Optional[int] = Field(default=None)
    
    fonte: str
    cidade: str
    descricao: str = ''