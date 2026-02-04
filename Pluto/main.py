from fastapi import (
    FastAPI,
)
from utils.defect_rate_medio import (get_defect_rate_medio,
                                     get_defect_rate_per_prodotto
                                     )
from utils.time_to_test_release import get_tempo_di_esecuzione_medio
from utils.tests_over_FTE import get_test_per_fte_data
import uvicorn
import os

app = FastAPI()

@app.get("/defect-rate-medio")
async def get_defect_rate_medio_endpoint():
    defect_rate = get_defect_rate_medio()
    return defect_rate

@app.get("/defect-rate-product")
async def get_defect_rate_product():
    return get_defect_rate_per_prodotto()

@app.get("/tempo-di-esecuzione-medio")
async def get_tempo_di_esecuzione_medio_endpoint():
    tempo_di_esecuzione_medio = get_tempo_di_esecuzione_medio()
    return tempo_di_esecuzione_medio['full']

@app.get("/tempo-di-esecuzione-medio-parziale")
async def get_tempo_di_esecuzione_medio_parziale_endpoint():
    tempo_di_esecuzione_medio = get_tempo_di_esecuzione_medio()
    return tempo_di_esecuzione_medio['partial']

@app.get("/montly-stat")
async def montly_stat():
    tempo_di_esecuzione_medio = get_tempo_di_esecuzione_medio()
    return tempo_di_esecuzione_medio['detailed_recap']

@app.get("/test-per-fte")
async def get_test_per_fte():
    general_tests_over_FTE = get_test_per_fte_data()
    return general_tests_over_FTE

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0",port=8000)