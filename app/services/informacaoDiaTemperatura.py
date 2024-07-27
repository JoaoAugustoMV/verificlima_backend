# from pydantic_sqlalchemy import sqlalchemy_to_pydantic
import asyncio, datetime
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

    async def get_all(self) -> List[InformacaoDiaTemperatura]:
        return await repository.get_all()
    
    def save_infos(self, infos: List[InformacaoDiaTemperatura]):
        return repository.insert_infos(infos)
    
    async def get_current_week(self):        
        all_week = self.__get_all_cd_dia_of_week()

        test = await self.get_payload_for_front(all_week)
        return test        
    
    async def get_payload_for_front(self, all_week: dict[int, date]) -> List[InformacaoDiaTemperatura]:
        coroutines = []
        for cd_dia, day_date in all_week.items():
            
            coroutines.append(self.__get_forecasts_payloads(cd_dia, day_date))
        results = await asyncio.gather(*coroutines)
        return [r for r in results if r ]        

    async def __get_forecasts_payloads(self, cd_dia, day_date):
        str_day = self.__return_str_day_forecast(cd_dia, day_date)
        # current = datetime.now()
        # print(cd_dia, day_date, 'start')
        infos_by_cd_dia = await self.get_infos_by_cd_dia(cd_dia)
        # print(cd_dia, day_date, 'end')
        # end = datetime.now()
        # diff = end - current
        # print(cd_dia, day_date, diff.seconds)
        if infos_by_cd_dia:                                
            return ForecastPayload(
                        madeIn=str_day, 
                        days_forecasts=self.__map_to_days_forecast(infos_by_cd_dia, str_day)
                    )
                    

    async def get_infos_by_cd_dia(self, cd_dia: int) -> List[InformacaoDiaTemperatura]:
        return await repository.get_by_cd_dia(cd_dia)        
    
    def __get_all_cd_dia_of_week(self) -> dict[int, date]:
        today = datetime.now()

        all_cd_dia = {}
        for a in range(0, DAYS_TO_ADD[-1] + 1):
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

    def __return_str_day_forecast(self, cd_dia: int, day_date: date) -> str:
        diff_cd_dia = self.today_cd_dia - cd_dia
        day_forecast_str = f'DIA {day_date.day}/{day_date.month} - {DAYS_OF_WEEK_PT_BR[day_date.weekday()]}'
        if diff_cd_dia == 0:
            day_forecast_str += f'(HOJE)'
        elif diff_cd_dia == 1:
            day_forecast_str += f'(AMANHA)'
    
        return f'{day_forecast_str}'        
            
    def __map_to_days_forecast(self, infos_by_cd_dia: List[InformacaoDiaTemperatura], str_day: str) -> List[DayForecast]:
        days_forecast = []
        for x_dias in DAYS_TO_ADD:
            infos_x_dias = [info for info in infos_by_cd_dia if info.x_dias == x_dias]
            if infos_x_dias:
                day_forecast_str = str_day
                forecastSources = self.__map_forecast_sources(infos_x_dias)
                days_forecast.append(
                    DayForecast(
                        day_forecasted=day_forecast_str,
                        forecast_made_in=f'{infos_x_dias[0].x_dias} dias atras',
                        forecast_sources=forecastSources)
                    )
                
        return days_forecast
       
    def __map_forecast_sources(self, infos: List[InformacaoDiaTemperatura]) -> List[ForecastSource]:
        forecastSources = []
        for info in infos:            
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