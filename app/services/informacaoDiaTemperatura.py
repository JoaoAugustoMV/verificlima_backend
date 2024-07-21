# from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from datetime import datetime, date, timedelta
from typing import List
from app.models.dayForecast import DayForecast
from app.models.forecastPayload import ForecastPayload
from app.models.forecastSource import ForecastSource
from app.repository.Repository import InfoRepository
from app.models.informacaoDiaTemperatura import InformacaoDiaTemperatura
from app.utils.configs import DAYS_OF_WEEK_PT_BR, DAYS_TO_ADD

repository = InfoRepository()

class InfoService():

    def retornarTodos(self) -> List[InformacaoDiaTemperatura]:
        return repository.retornarTodos()
    
    def salvarInfos(self, infos: List[InformacaoDiaTemperatura]):
        return repository.inserirInfos(infos)
    
    def get_current_week(self):        
        all_week = self.__get_all_cd_dia_of_week()

        return self.get_payload_for_front(all_week)        
    
    def get_payload_for_front(self, all_week: dict[int, date]) -> List[InformacaoDiaTemperatura]:
        payloads = []
        for cd_dia, day in all_week.items():
            
            madeIn = self.__made_in_by_cd_dia(cd_dia, day)
            days_infos = self.get_infos_by_cd_dia(cd_dia)
            if days_infos:                
                test = self.__mapper_to_front(days_infos)
                payloads.append(ForecastPayload(madeIn=madeIn, daysForecasts=test))
        return payloads

    def get_infos_by_cd_dia(self, cd_dia: int) -> List[InformacaoDiaTemperatura]:
        info = repository.retornarPorCdDia(cd_dia)
        return info.all()        
    
    def __get_all_cd_dia_of_week(self) -> dict[int, date]:
        today = datetime.now()

        all_cd_dia = {}
        for a in range(0, DAYS_TO_ADD[-1]):
            day = (today + timedelta(days=a)).date()
            if day.day < 10:
                day_str = f'0{day.day}'
            else:
                day_str = day.day

            if day.month < 10:
                month_str = f'0{day.month}'
            else:
                month_str = day.month

            cd_dia = int(f'{day.year}{month_str}{day_str}')

            if a == 0:
                self.today_cd_dia = cd_dia
            all_cd_dia[cd_dia] = day

        return all_cd_dia

    def __made_in_by_cd_dia(self, cd_dia: int, day: date) -> str:
        diff_cd_dia = self.today_cd_dia - cd_dia
        if diff_cd_dia == 0:
            return 'Hoje'
        elif diff_cd_dia == 1:
            return 'Amanha'
        else:
            return DAYS_OF_WEEK_PT_BR[day.weekday()]
            
    def __mapper_to_front(self, infos: List[InformacaoDiaTemperatura]) -> List[DayForecast]:
        days_forecast = []
        for x_dias in DAYS_TO_ADD:
            infos_x_dias = [info for info in infos if info.x_dias == x_dias]
            if infos_x_dias:
                day_forecast_str = self.__get_day_forecasted(infos_x_dias[0].cd_dia, x_dias)
                forecastSources = self.__get_forecastSources(infos_x_dias)
                days_forecast.append(DayForecast(dayForecasted=day_forecast_str, forecastMadeIn=f'{infos_x_dias[0].x_dias} dias atras', forecastSources=forecastSources))
        return days_forecast

    def __get_day_forecasted(self, cd_dia:int, x_dias: int) -> str:
        today = datetime.now()
        day = (today + timedelta(days=x_dias)).date()
        day_forecast_str = f'DIA {day.day}/{day.month} - {DAYS_OF_WEEK_PT_BR[day.weekday()]}'
        if x_dias == 0:
            day_forecast_str += f'(HOJE)'
        elif x_dias == 1:
            day_forecast_str += f"(AMANHA)"

        return day_forecast_str
#   
    def __get_forecastSources(self, infos: List[InformacaoDiaTemperatura]) -> List[ForecastSource]:
        forecastSources = []
        for info in infos:
            # TODO criar logica das fontes de dados
            if int(info.x_dias) == 0:
                forecastSource = ForecastSource(
                    name=info.fonte,
                    urlSite=info.fonte, 
                    minTemperature=int(info.temperatura_real_min),
                    maxTemperature=int(info.temperatura_real_max)
                )
            else:
                forecastSource = ForecastSource(
                    name=info.fonte, 
                    urlSite=info.fonte, 
                    minTemperature=int(info.temperatura_min_previsao_feita_menos_x),
                    maxTemperature=int(info.temperatura_max_previsao_feita_menos_x)
                )
            forecastSources.append(forecastSource)
        return forecastSources
#     "id": "20",
#     "cd_dia": "20240718",
#     "x_dias": "0",
#     "dia_previsao_feita_menos_x": None,
#     "temperatura_min_previsao_feita_menos_x": None,
#     "temperatura_max_previsao_feita_menos_x": None,
#     "temperatura_real_min": "12",
#     "temperatura_real_max": "24",
#     "fonte": "APIADVISOR",
#     "cidade": "SAO PAULO",
#     "descricao": "",
#     "dt_inclusao": "2024-07-18 22:19:27.233428"
#   }

#   {
#     "id": "16",
#     "cd_dia": "20240718",
#     "x_dias": "0",
#     "dia_previsao_feita_menos_x": "2024-07-18",
#     "temperatura_min_previsao_feita_menos_x": None,
#     "temperatura_max_previsao_feita_menos_x": None,
#     "temperatura_real_min": "15",
#     "temperatura_real_max": "24",
#     "fonte": "HGBrasil",
#     "cidade": "SAO PAULO",
#     "descricao": "Tempo limpo",
#     "dt_inclusao": "2024-07-18 22:19:27.233428"
#   }

    def mock(self):
        mock_resp =  [
            {
                "id": "13",
                "cd_dia": "20240723",
                "x_dias": "5",
                "dia_previsao_feita_menos_x": "2024-07-18",
                "temperatura_min_previsao_feita_menos_x": "17",
                "temperatura_max_previsao_feita_menos_x": "25",
                "temperatura_real_min": None,
                "temperatura_real_max": None,
                "fonte": "HGBrasil",
                "cidade": "SAO PAULO",
                "descricao": "Tempo limpo",
                "dt_inclusao": "2024-07-18 22:19:27.233428"
            },
            {
                "id": "14",
                "cd_dia": "20240721",
                "x_dias": "3",
                "dia_previsao_feita_menos_x": "2024-07-18",
                "temperatura_min_previsao_feita_menos_x": "13",
                "temperatura_max_previsao_feita_menos_x": "24",
                "temperatura_real_min": None,
                "temperatura_real_max": None,
                "fonte": "HGBrasil",
                "cidade": "SAO PAULO",
                "descricao": "Tempo limpo",
                "dt_inclusao": "2024-07-18 22:19:27.233428"
            },
            {
                "id": "15",
                "cd_dia": "20240719",
                "x_dias": "1",
                "dia_previsao_feita_menos_x": "2024-07-18",
                "temperatura_min_previsao_feita_menos_x": "14",
                "temperatura_max_previsao_feita_menos_x": "23",
                "temperatura_real_min": None,
                "temperatura_real_max": None,
                "fonte": "HGBrasil",
                "cidade": "SAO PAULO",
                "descricao": "Tempo limpo",
                "dt_inclusao": "2024-07-18 22:19:27.233428"
            },
            {
                "id": "16",
                "cd_dia": "20240718",
                "x_dias": "0",
                "dia_previsao_feita_menos_x": "2024-07-18",
                "temperatura_min_previsao_feita_menos_x": None,
                "temperatura_max_previsao_feita_menos_x": None,
                "temperatura_real_min": "15",
                "temperatura_real_max": "24",
                "fonte": "HGBrasil",
                "cidade": "SAO PAULO",
                "descricao": "Tempo limpo",
                "dt_inclusao": "2024-07-18 22:19:27.233428"
            },
            {
                "id": "17",
                "cd_dia": "20240723",
                "x_dias": "5",
                "dia_previsao_feita_menos_x": "2024-07-18",
                "temperatura_min_previsao_feita_menos_x": "11",
                "temperatura_max_previsao_feita_menos_x": "24",
                "temperatura_real_min": None,
                "temperatura_real_max": None,
                "fonte": "APIADVISOR",
                "cidade": "SAO PAULO",
                "descricao": "",
                "dt_inclusao": "2024-07-18 22:19:27.233428"
            },
            {
                "id": "18",
                "cd_dia": "20240721",
                "x_dias": "3",
                "dia_previsao_feita_menos_x": "2024-07-18",
                "temperatura_min_previsao_feita_menos_x": "12",
                "temperatura_max_previsao_feita_menos_x": "24",
                "temperatura_real_min": None,
                "temperatura_real_max": None,
                "fonte": "APIADVISOR",
                "cidade": "SAO PAULO",
                "descricao": "",
                "dt_inclusao": "2024-07-18 22:19:27.233428"
            },
            {
                "id": "19",
                "cd_dia": "20240719",
                "x_dias": "1",
                "dia_previsao_feita_menos_x": "2024-07-18",
                "temperatura_min_previsao_feita_menos_x": "13",
                "temperatura_max_previsao_feita_menos_x": "22",
                "temperatura_real_min": None,
                "temperatura_real_max": None,
                "fonte": "APIADVISOR",
                "cidade": "SAO PAULO",
                "descricao": "",
                "dt_inclusao": "2024-07-18 22:19:27.233428"
            },
            {
                "id": "20",
                "cd_dia": "20240718",
                "x_dias": "0",
                "dia_previsao_feita_menos_x": None,
                "temperatura_min_previsao_feita_menos_x": None,
                "temperatura_max_previsao_feita_menos_x": None,
                "temperatura_real_min": "12",
                "temperatura_real_max": "24",
                "fonte": "APIADVISOR",
                "cidade": "SAO PAULO",
                "descricao": "",
                "dt_inclusao": "2024-07-18 22:19:27.233428"
            }
            ]
        
        resp = []
        for m in mock_resp:
            resp.append(InformacaoDiaTemperatura(**m))

        self.resp: List[InformacaoDiaTemperatura] = resp

    