from fastapi import FastAPI
from backend.app.api.endpoints import relatorio_geral

app = FastAPI()

app.include_router(relatorio_geral.router)
