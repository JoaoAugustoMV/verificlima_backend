import logging

from sqlalchemy import exc
from fastapi import FastAPI, Request

from app.repository.Repository import InfoRepository
from app.routers.informacaoDiaTemperatura import router as infoDiaTemp
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

@app.middleware('http')
async def try_db(request: Request, call_next):
    try:            
        response = await call_next(request)
        return response
    
    except exc.SQLAlchemyError as e:
        infoRepo = InfoRepository()
        logging.info("Reconnect the session")
        infoRepo.session = infoRepo.get_session()
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