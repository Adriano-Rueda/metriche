from fastapi import (
    FastAPI,
)
from utils.defect_rate_medio import get_defect_rate_medio
from utils.time_to_test_release import get_tempo_di_esecuzione_medio
import uvicorn
import os

app = FastAPI()

@app.get("/defect-rate-medio")
async def get_defect_rate_medio_endpoint():
    defect_rate = get_defect_rate_medio()
    return defect_rate



@app.get("/tempo-di-esecuzione-medio")
async def get_tempo_di_esecuzione_medio_endpoint():
    tempo_di_esecuzione_medio = get_tempo_di_esecuzione_medio()
    return tempo_di_esecuzione_medio['full']

@app.get("/tempo-di-esecuzione-medio-parziale")
async def get_tempo_di_esecuzione_medio_parziale_endpoint():
    tempo_di_esecuzione_medio = get_tempo_di_esecuzione_medio()
    return tempo_di_esecuzione_medio['partial']

@app.get("/test-per-fte")
async def get_test_per_fte():
    return {"message": "Test per FTE endpoint"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0",port=8000)