from sqlalchemy import Column, Integer, String, DateTime, func
from .database import Base

class Empresa(Base):
    """
    Modelo ORM que representa a tabela 'empresas' no banco de dados.
    """
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    cnpj = Column(String, unique=True, index=True, nullable=False)
    cidade = Column(String, index=True)
    ramo_atuacao = Column(String, index=True)
    telefone = Column(String, nullable=False)
    email_contato = Column(String, unique=True, index=True, nullable=False)
    data_cadastro = Column(DateTime(timezone=True), server_default=func.now())

class Usuario(Base):
    """
    Modelo ORM que representa a tabela 'usuarios' (administradores) no banco de dados.
    """
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
