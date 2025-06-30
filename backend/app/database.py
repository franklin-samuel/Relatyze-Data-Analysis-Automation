from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models import RelatorioSocial, Base
import uuid

DATABASE_URL = "postgresql://postgres:Kkkrsrsrs28?@localhost:5432/relatorios_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def criar_tabelas():
    Base.metadata.create_all(bind=engine)

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