from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models import RelatorioSocial, TokenSocial, Base
from datetime import datetime, UTC
import uuid

DATABASE_URL = "postgresql://postgres:Kkkrsrsrs28?@localhost:5432/relatorios_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#-----|Banco de dados -> Relatórios|-----
def criar_relatorio(db: Session, relatorio: RelatorioSocial) -> RelatorioSocial:
    db.add(relatorio)
    db.commit()
    db.refresh(relatorio)
    return relatorio

def listar_relatorios(db: Session):
    return db.query(RelatorioSocial).all()

def buscar_relatorio_por_id(db: Session, relatorio_id: uuid.UUID):
    return db.query(RelatorioSocial).filter(RelatorioSocial.id == relatorio_id).first()

def atualizar_relatorio(db: Session, relatorio_id: uuid.UUID, dados: dict):
    relatorio = buscar_relatorio_por_id(db, relatorio_id)
    if not relatorio:
        return None
    
    for chave, valor in dados.items():
        setattr(relatorio, chave, valor)
    db.commit()
    db.refresh(relatorio)
    return relatorio

def deletar_relatorio(db: Session, relatorio_id: uuid.UUID):
    relatorio = buscar_relatorio_por_id(db, relatorio_id)
    if not relatorio:
        return False
    db.delete(relatorio)
    db.commit()
    return True

#-----|Banco de dados -> Tokens|-----
def salvar_token(db: Session, rede_social: str, token: str):
    token = token.encode("utf-8", errors="ignore").decode("utf-8")
    rede_social = rede_social.encode("utf-8", errors="ignore").decode("utf-8")

    tokens_existente = db.query(TokenSocial).filter(TokenSocial.rede_social == rede_social).first()

    if tokens_existente:
        tokens_existente.token = token
        tokens_existente.atualizado_em = datetime.now(UTC)
    else:
        novo_token = TokenSocial(
            rede_social=rede_social,
            token=token,
            atualizado_em=datetime.now(UTC)
        )
        db.add(novo_token)
    db.commit()

def obter_token(db: Session, rede_social: str) -> str | None:
    token = db.query(TokenSocial).filter(TokenSocial.rede_social == rede_social).first()
    return token.token if token else None
    
    
