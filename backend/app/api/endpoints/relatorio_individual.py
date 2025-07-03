from fastapi import APIRouter, HTTPException
from uuid import UUID
from typing import List
from app.models import RelatorioSocial
from app.core import relatorio_crud

router = APIRouter()

@router.get("/relatorios", response_model=List[RelatorioSocial])
def listar_relatorios():
    return relatorio_crud.obter_todos_relatorios()

@router.get("/relatorios/{relatorio_id}", response_model=RelatorioSocial)
def obter_relatorio(relatorio_id: UUID):
    relatorio = relatorio_crud.obter_relatorio_por_id(relatorio_id)
    if not relatorio:
        raise HTTPException(status_code=404, detail="Relátorio não encontrado")
    return relatorio

@router.post("/relatorios", response_model=RelatorioSocial)
def criar_relatorio(relatorio: RelatorioSocial):
    return relatorio_crud.criar_novo_relatorio(relatorio.dict())

@router.put("relatorios/{relatorio_id}", response_model=RelatorioSocial)
def atualizar_relatorio(relatorio_id: UUID, dados: RelatorioSocial):
    relatorio_atualizado = relatorio_crud.atualizar_relatorio_existente(relatorio_id, dados.dict())
    if not relatorio_atualizado:
        raise HTTPException(status_code=404, detail="Relátorio não encontrado para atualizar")