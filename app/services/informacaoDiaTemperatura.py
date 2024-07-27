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

    def get_all(self) -> List[InformacaoDiaTemperatura]:
        return repository.get_all()
    
    def save_infos(self, infos: List[InformacaoDiaTemperatura]):
        return repository.insert_infos(infos)
    
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
                payloads.append(ForecastPayload(madeIn=madeIn, days_forecasts=test))
        return payloads

    def get_infos_by_cd_dia(self, cd_dia: int) -> List[InformacaoDiaTemperatura]:
        info = repository.get_by_cd_dia(cd_dia)
        return info
    
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
                forecastSources = self.__get_forecast_sources(infos_x_dias)
                days_forecast.append(DayForecast(day_forecasted=day_forecast_str, forecast_made_in=f'{infos_x_dias[0].x_dias} dias atras', forecast_sources=forecastSources))
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
    def __get_forecast_sources(self, infos: List[InformacaoDiaTemperatura]) -> List[ForecastSource]:
        forecastSources = []
        for info in infos:
            # TODO criar logica das fontes de dados?
            if int(info.x_dias) == 0:
                forecastSource = ForecastSource(
                    name=info.fonte,
                    url_site=info.fonte, 
                    min_temperature=int(info.temperatura_real_min),
                    max_temperature=int(info.temperatura_real_max)
                )
            else:
                forecastSource = ForecastSource(
                    name=info.fonte, 
                    url_site=info.fonte, 
                    min_temperature=int(info.temperatura_min_previsao_feita_menos_x),
                    max_temperature=int(info.temperatura_max_previsao_feita_menos_x)
                )
            forecastSources.append(forecastSource)
        return forecastSources