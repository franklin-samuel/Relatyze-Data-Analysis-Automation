import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from app.core.relatorio_coletor import coletar_relatorio_geral
from datetime import datetime
from fastapi.responses import StreamingResponse

PASTA_PDFS = "C:\Users\samue\Documents\Relatórios Semanais PDFs"

def gerar_nome_pdf():
    hoje = datetime.now()
    semana = hoje.strftime("semana_%Y-%W")
    nome = f"relatorio_{semana}.pdf"
    return nome

def gerar_pdf_relatorio() -> tuple[BytesIO, str]:
    dados = coletar_relatorio_geral()
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Relatório Semanal Mídias Sociais")
    y -= 40

    c.setFont("Helvetica", 12)

    for rede, valores in dados.items():
        c.drawString(50, y, f"📱 {rede.upper()}")
        y -= 20
        for chave, valor in valores.items():
            c.drawString(70, y, f"{chave.replace('_', ' ').capitalize()}: {valor}")
            y -= 18
        y -= 10

        if y < 100:
            c.showPage()
            y = height - 50
    
    c.save()
    buffer.seek(0)

    os.makedirs(PASTA_PDFS, exist_ok=True)

    nome_arquivo = gerar_nome_pdf()
    caminho_arquivo = os.path.join(PASTA_PDFS, nome_arquivo)

    with open(caminho_arquivo, "wb") as f:
        f.write(buffer.getbuffer())
    
    buffer.seek(0)
    return buffer, nome_arquivo

def baixar_relatorio():
    pdf_buffer, nome_arquivo = gerar_pdf_relatorio()
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={nome_arquivo}"})

        

