import base64
import requests
from io import BytesIO
from app.config import ULTRAMSG_INSTANCE_ID, ULTRAMSG_TOKEN

def enviar_pdf_whatsapp(numero: str, pdf: BytesIO, nome_arquivo: str) -> bool:
    print(f"[Whatsapp] Enviando PDF '{nome_arquivo} para {numero}'")

    pdf_base64 = base64.b64encode(pdf.read()).decode("utf-8")
    
    url = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE_ID}/messages/document"

    payload = {
        "token": ULTRAMSG_TOKEN,
        "to": numero,
        "filename": nome_arquivo,
        "document": f"data:application/pdf;base64,{pdf_base64}"
    }

    response = requests.post(url, data=payload)
    print(f"[Whatsapp] Status: {response.status_code} - {response.text}")

    return response.status_code == 200