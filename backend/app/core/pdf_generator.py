from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from app.core.relatorio_coletor import coletar_relatorio_geral

def gerar_pdf_relatorio() -> BytesIO:
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
    return buffer
        

