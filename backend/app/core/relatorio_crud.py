from app.database import SessionLocal, criar_relatorio, listar_relatorios, buscar_relatorio_por_id, atualizar_relatorio, deletar_relatorio
from app.models import RelatorioSocial
import uuid

def obter_todos_relatorios():
    db = SessionLocal()
    relatorios = listar_relatorios(db)
    db.close()
    return relatorios

def obter_relatorio_por_id():
    db = SessionLocal()
    relatorio = buscar_relatorio_por_id(db, relatorio)
    db.close()
    return relatorio

def criar_novo_relatorio(dados: dict):
    db = SessionLocal()
    novo_relatorio = RelatorioSocial(**dados)
    relatorio = criar_relatorio(db, novo_relatorio)
    db.close()
    return relatorio

def atualizar_relatorio_existente(relatorio_id: uuid.UUID, dados: dict):
    db = SessionLocal()
    relatorio = atualizar_relatorio(db, relatorio_id, dados)
    db.close()
    return relatorio

def deletar_relatorio_existente(relatorio_id: uuid.UUID):
    db = SessionLocal()
    sucesso = deletar_relatorio(db, relatorio_id)
    db.close()
    return sucesso
