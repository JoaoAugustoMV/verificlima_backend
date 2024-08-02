import asyncio
import logging

from sqlalchemy import exc
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.repository.Repository import InfoRepository
from app.routers.informacaoDiaTemperatura import router as infoDiaTemp
from app.routers.BFF import router as bff
from app.utils.keep_alive import keep_alive_session
from app.utils.setup_logs import setup_logging

async def main():
    setup_logging()
    await keep_alive_session()

loop = asyncio.get_event_loop()
loop.create_task(main())
app = FastAPI(
    title="VerifiClima Backend",
    description='Descrição',
    summary='sumario',
    contact=
        {
            "name": "GitHub - verificlima_backend",
            "url": "http://x-force.example.com/contact/"
        }
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware('http')
async def try_db(request: Request, call_next):
    try:            
        response = await call_next(request)
        return response
    
    except exc.SQLAlchemyError as e:
        info_repo = InfoRepository()
        logging.info("Reconnect the session")
        info_repo.session = info_repo.get_session()
        logging.info("Retry with new session")

    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logging.error("", e)
        raise e

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(infoDiaTemp)
app.include_router(bff)
