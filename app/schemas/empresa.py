# Importações necessárias do Pydantic para criação de modelos e validação,
# do datetime para manipulação de datas, e do typing para anotações de tipo.
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class EmpresaBase(BaseModel):
    """
    Schema Pydantic base que define os campos comuns e as regras de validação
    para a entidade Empresa. Todos os outros schemas de empresa herdam desta base.
    """
    # Field(..., min_length=3, ...) define que o campo é obrigatório (...) e tem um tamanho mínimo.
    # 'example' é usado para a documentação automática do Swagger UI.
    nome: str = Field(..., min_length=3, example="Empresa Exemplo S.A.")
    cnpj: str = Field(..., min_length=14, max_length=14, example="12345678000195")
    cidade: str
    ramo_atuacao: str
    telefone: str
    # EmailStr é um tipo especial do Pydantic que valida automaticamente se a string é um formato de e-mail válido.
    email_contato: EmailStr

class EmpresaCreate(EmpresaBase):
    """
    Schema usado especificamente para a criação de uma nova empresa.
    Herda todos os campos de EmpresaBase.
    'pass' indica que não há campos adicionais necessários para a criação.
    """
    pass

class EmpresaUpdate(BaseModel):
    """
    Schema para a atualização de uma empresa.
    Todos os campos são definidos como Optional, o que significa que não são obrigatórios.
    Isto permite que o cliente da API envie apenas os campos que deseja alterar (atualização parcial).
    """
    nome: Optional[str] = Field(None, min_length=3)
    cidade: Optional[str] = None
    ramo_atuacao: Optional[str] = None
    telefone: Optional[str] = None
    email_contato: Optional[EmailStr] = None

class Empresa(EmpresaBase):
    """
    Schema usado para as respostas da API (leitura de dados).
    Herda todos os campos de EmpresaBase e adiciona os campos que são gerados
    pela base de dados (como 'id' e 'data_cadastro').
    """
    id: int
    data_cadastro: datetime
    
    class Config:
        """
        Configurações internas do modelo Pydantic.
        """
        # 'from_attributes = True' (anteriormente orm_mode) permite que o Pydantic
        # leia os dados diretamente de um objeto ORM do SQLAlchemy,
        # facilitando a conversão do modelo da base de dados (models.Empresa) para o schema Pydantic.
        from_attributes = True

