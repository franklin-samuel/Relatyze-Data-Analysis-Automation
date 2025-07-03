from fastapi import APIRouter, HTTPException
from uuid import UUID
from typing import List
from app.schemas.relatorio import RelatorioSocialOut, RelatorioSocialCreate
from app.core import relatorio_crud

router = APIRouter()

@router.get("/relatorios", response_model=List[RelatorioSocialOut])
def listar_relatorios():
    return relatorio_crud.obter_todos_relatorios()

@router.get("/relatorios/{relatorio_id}", response_model=RelatorioSocialOut)
def obter_relatorio(relatorio_id: UUID):
    relatorio = relatorio_crud.obter_relatorio_por_id(relatorio_id)
    if not relatorio:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    return relatorio

@router.post("/relatorios", response_model=RelatorioSocialOut)
def criar_relatorio(relatorio: RelatorioSocialCreate):
    return relatorio_crud.criar_novo_relatorio(relatorio.dict())

@router.put("/relatorios/{relatorio_id}", response_model=RelatorioSocialOut)
def atualizar_relatorio(relatorio_id: UUID, dados: RelatorioSocialCreate):
    relatorio_atualizado = relatorio_crud.atualizar_relatorio_existente(relatorio_id, dados.dict())
    if not relatorio_atualizado:
        raise HTTPException(status_code=404, detail="Relatório não encontrado para atualizar")
    return relatorio_atualizado

@router.delete("/relatorios/{relatorio_id}")
def deletar_relatorio(relatorio_id: UUID):
    sucesso = relatorio_crud.deletar_relatorio_existente(relatorio_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Relatório não encontrado para excluir")
    return {"mensagem": "Relatório excluído com sucesso"}
