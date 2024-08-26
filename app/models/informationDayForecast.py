from pydantic import BaseModel

class InformationDayForecast(BaseModel):
    id: str = None
    cd_dia: int
    x_dias: int = None
    dia_previsao_feita_menos_x: str = None
    temperatura_min_previsao_feita_menos_x: int = None
    temperatura_max_previsao_feita_menos_x: int = None
    
    temperatura_real_min: int = None
    temperatura_real_max: int = None
    
    fonte: str
    cidade: str
    descricao: str = ''