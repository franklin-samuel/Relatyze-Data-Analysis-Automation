from app.services.instagram_service import obter_relatorio_semanal_instagram
from app.services.facebook_service import obter_relatorio_semanal_facebook
from app.services.youtube_service import obter_relatorio_semanal_youtube
from app.database import SessionLocal, criar_relatorio
from app.models import RelatorioSocial, OrigemDadosEnum
from datetime import datetime, UTC

def coletar_todos_relatorios(access_token_youtube: str):
    db = SessionLocal()
    hoje = datetime.now(UTC)