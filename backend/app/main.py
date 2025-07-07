from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import relatorio_geral, relatorio_individual, youtube, diagnostico

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(relatorio_geral.router)
app.include_router(relatorio_individual.router)
app.include_router(youtube.router)
app.include_router(diagnostico.router)
