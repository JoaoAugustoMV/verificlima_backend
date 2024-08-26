import asyncio
from app.models.informationDayForecast import InformationDayForecast
from app.utils.SingletonMeta import SingletonMeta
from azure.cosmos.aio import CosmosClient
from app.utils.configs import KEY_COSMO_DB, URI_COSMO_DB


client = CosmosClient(url=URI_COSMO_DB, credential=KEY_COSMO_DB)
db = client.get_database_client('database-cosmodb-verificlima')
class InfoRepository(metaclass=SingletonMeta):
    def __init__(self) -> None:        
        self.container = db.get_container_client('container-cosmodb-verificlima')
        
    async def   insert_infos(self, infos: list[InformationDayForecast]):                        
        inserts_func = [self.container.upsert_item(i.model_dump()) for i in infos]
        resp = await asyncio.gather(*inserts_func)
        
        return resp