from fastapi import APIRouter, Query
from app.core.relatorio_coletor import coletar_relatorio_geral

router = APIRouter()

@router.get("relatorios/geral")
def relatorio_geral():
    return coletar_relatorio_geral()