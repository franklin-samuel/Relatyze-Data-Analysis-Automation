from fastapi import APIRouter, Body, HTTPException
from app.services.youtube_service import trocar_codigo_por_token
from app.database import salvar_token, SessionLocal

router = APIRouter()

@router.post("/auth/youtube")
def autenticar_youtube(codigo: str = Body(..., embed=True)):
    dados = trocar_codigo_por_token(codigo)

    if not dados or "access_token" not in dados:
        raise HTTPException(status_code=400, detail={
            "erro": "Falha ao obter token do YouTube",
            "resposta": dados
        })

    access_token = dados["access_token"]

    db = SessionLocal()
    salvar_token(db, "youtube", access_token)
    db.close()

    return {
        "mensagem": "Token do YouTube salvo com sucesso",
        "dados": {
            "access_token": access_token,
            "expires_in": dados.get("expires_in"),
            "refresh_token": dados.get("refresh_token")
        }
    }
