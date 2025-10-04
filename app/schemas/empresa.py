from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class EmpresaBase(BaseModel):
    nome: str = Field(..., min_length=3, example="Empresa Exemplo S.A.")
    cnpj: str = Field(..., min_length=14, max_length=14, example="12345678000195")
    cidade: str
    ramo_atuacao: str
    telefone: str
    email_contato: EmailStr

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3)
    cidade: Optional[str] = None
    ramo_atuacao: Optional[str] = None
    telefone: Optional[str] = None
    email_contato: Optional[EmailStr] = None

class Empresa(EmpresaBase):
    id: int
    data_cadastro: datetime
    class Config:
        from_attributes = True