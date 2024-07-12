
from fastapi import FastAPI

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

app.include_router(infoDiaTemp)

@app.get("/")
async def root():
    return {"message": "Hello World"}