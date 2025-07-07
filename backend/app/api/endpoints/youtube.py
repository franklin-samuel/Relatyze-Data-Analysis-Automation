from fastapi import APIRouter, Request, Body
from app.services.youtube_service import trocar_codigo_por_token
from app.database import salvar_token, SessionLocal

router = APIRouter()

@router.post("/auth/youtube")
def autenticar_youtube(codigo: str = Body(..., embed=True)):
    dados = trocar_codigo_por_token(codigo)
    access_token = dados.get("access_token")

    if not access_token:
        return {"erro": "Falha ao obter token", "detalhes": dados}

    db = SessionLocal()
    salvar_token(db, "youtube", access_token)
    db.close()

    return {"mensagem": "Token do YouTube salvo com sucesso"}