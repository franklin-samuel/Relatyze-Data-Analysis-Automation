from sqlalchemy import Column, String, Integer,  Float, Date, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import enum
import uuid

Base = declarative_base()

class OrigemDadosEnum(str, enum.Enum):
    manual = "manual"
    api = "api"

class RelatorioSocial(Base):
    __tablename__ = "relatorios_sociais"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    rede_social = Column(String, nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)
    seguidores_inicio = Column(Integer, nullable=False)
    seguidores_fim = Column(Integer, nullable=False)
    publicacoes = Column(Integer, nullable=False)
    alcance_total = Column(Integer, nullable=False)
    engajamento = Column(Integer, nullable=False)
    origem = Column(Enum(OrigemDadosEnum), nullable=False)
