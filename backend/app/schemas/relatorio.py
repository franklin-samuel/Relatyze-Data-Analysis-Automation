from pydantic import BaseModel
from uuid import UUID
from datetime import date
from enum import Enum
from typing import List

class OrigemDadosEnum(str, Enum):
    manual = "manual"
    api = "api"

class RelatorioSocialOut(BaseModel):
    id: UUID
    rede_social: str
    data_inicio: date
    data_fim: date
    seguidores_inicio: int
    seguidores_fim: int
    publicacoes: int
    alcance_total: int
    engajamento: float
    origem: OrigemDadosEnum

    class Config:
        orm_mode = True

class RelatorioSocialCreate(BaseModel):
    rede_social: str
    data_inicio: date
    data_fim: date
    seguidores_inicio: int
    seguidores_fim: int
    publicacoes: int
    alcance_total: int
    engajamento: float
    origem: OrigemDadosEnum
