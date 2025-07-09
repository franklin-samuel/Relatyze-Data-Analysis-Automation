from fastapi import APIRouter, Query, Body
from fastapi.responses import StreamingResponse
from app.core.relatorio_coletor import coletar_relatorio_geral
from app.core.pdf_generator import gerar_pdf_relatorio, baixar_relatorio
from app.core.relatorio_whatsapp import gerar_e_enviar_relatorio

router = APIRouter()

@router.get("/relatorios/geral")
def relatorio_geral():
    return coletar_relatorio_geral()

@router.get("/relatorios/geral/baixar_pdf")
def baixar_relatorio_geral_pdf():
    return baixar_relatorio()

@router.post("/relatorios/enviar-whatsapp")
def enviar_relatorio_whatsapp(numero: str = Body(..., embed=True)):
    return gerar_e_enviar_relatorio(numero)