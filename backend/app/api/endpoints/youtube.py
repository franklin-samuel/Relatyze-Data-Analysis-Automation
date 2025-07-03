from fastapi import APIRouter, Request
from app.services.youtube_service import trocar_codigo_por_token
from app.database import salvar_token, SessionLocal

router = APIRouter()

@router.get("/oauth2callback")
def oauth_callback(code:str):
    db = SessionLocal()
    dados_token = trocar_codigo_por_token(code)
    access_token = dados_token.get("access_token")

    if not access_token:
        return {"erro": "Falha ao obter token"}
    
    salvar_token(db, "youtube", access_token)
    return {"mensagem": "Token salvo com sucesso"}