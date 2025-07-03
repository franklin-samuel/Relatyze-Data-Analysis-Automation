from fastapi import FastAPI
from app.api.endpoints import relatorio_geral, relatorio_individual

app = FastAPI()

app.include_router(relatorio_geral.router)
app.include_router(relatorio_individual.router)
