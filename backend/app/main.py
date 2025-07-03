from fastapi import FastAPI
from app.api.endpoints import relatorios

app = FastAPI()

app.include_router(relatorios.router)
