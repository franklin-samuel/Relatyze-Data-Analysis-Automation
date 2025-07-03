from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from app.core.relatorio_coletor import coletar_relatorio_geral
from app.core.pdf_generator import gerar_pdf_relatorio

router = APIRouter()

@router.get("/relatorios/geral")
def relatorio_geral():
    return coletar_relatorio_geral()

@router.get("/relatorios/geral/pdf")
def baixar_relatorio_geral_pdf():
    pdf_buffer = gerar_pdf_relatorio()
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=relatorio_geral.pdf"})