from datetime import datetime, date

from sqlmodel import  SQLModel, Field

class InformacaoDiaTemperatura(SQLModel, table=True):
    __tablename__ = "informacao_previsao_temperatura"

    id: int = Field(default=None, primary_key=True)
    cd_dia: int
    x_dias: int
 
    dia_previsao_feita_menos_x: date =  None
    temperatura_min_previsao_feita_menos_x: int =  None
    temperatura_max_previsao_feita_menos_x: int =  None
    
    temperatura_real_min: int =  None
    temperatura_real_max: int =  None
    
    fonte: str
    cidade : str
    descricao : str =  ''

    dt_inclusao: str =  str(datetime.now())