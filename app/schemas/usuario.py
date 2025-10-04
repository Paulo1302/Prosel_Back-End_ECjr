from pydantic import BaseModel, Field

class UsuarioBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=6)

class Usuario(UsuarioBase):
    id: int
    class Config:
        from_attributes = True