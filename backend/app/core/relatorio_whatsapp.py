from app.services.whatsapp_service import enviar_pdf_whatsapp
from app.core.pdf_generator import gerar_pdf_relatorio

def gerar_e_enviar_relatorio(numero_whatsapp: str) -> dict:
    print("[Relatório Whatsapp] Iniciando processo de geração e envio do relatório...")

    try:
        pdf, nome_arquivo = gerar_pdf_relatorio()
        print(f"[Relatório Whatsapp] PDF {nome_arquivo} gerado com sucesso.")

        sucesso = enviar_pdf_whatsapp(numero_whatsapp, pdf, nome_arquivo)

        if sucesso:
            print("[Relatório Whatsapp] Relatório enviado com sucesso via Whatsapp.")
            return {"mensagem": "Relátorio gerado e enviado com sucesso via Whatsapp."}
        else:
            print("[Relátorio Whatsapp] Falha ao enviar o relátorio via Whatsapp")
            return {"erro": "Falha ao enviar o relátorio via Whatsapp"}
        
    except Exception as e:
        print(f"[Relatório Whatsapp] Erro inesperado: {e}")
        return {"erro": f"Erro inesperado: {e}"}