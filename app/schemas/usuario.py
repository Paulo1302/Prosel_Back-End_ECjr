# Importa o BaseModel do Pydantic, a classe base para todos os modelos de validação de dados,
# e o Field para adicionar validações extras aos campos.
from pydantic import BaseModel, Field

class UsuarioBase(BaseModel):
    """
    Schema Pydantic base que define os campos e validações comuns para um utilizador.
    """
    # Define o campo 'username' com validações:
    # - ... (elipse): Indica que o campo é obrigatório.
    # - min_length/max_length: Define o intervalo de tamanho permitido para o nome de utilizador.
    username: str = Field(..., min_length=3, max_length=50)

class UsuarioCreate(UsuarioBase):
    """
    Schema usado especificamente para o registo de um novo utilizador.
    Herda o 'username' de UsuarioBase e adiciona o campo 'password'.
    """
    # Define o campo 'password' com uma validação de tamanho mínimo.
    # Este schema é usado para validar os dados que chegam no corpo do pedido de /register.
    password: str = Field(..., min_length=6)

class Usuario(UsuarioBase):
    """
    Schema usado para as respostas da API que retornam dados de um utilizador.
    Herda o 'username' de UsuarioBase e adiciona o 'id' da base de dados.
    
    Importante: Este modelo NÃO inclui o campo 'password', garantindo que a senha
    (mesmo que hasheada) nunca seja exposta nos endpoints da API.
    """
    id: int
    
    class Config:
        """
        Configurações internas do modelo Pydantic.
        """
        # 'from_attributes = True' (anteriormente orm_mode) permite que o Pydantic
        # leia os dados diretamente de um objeto ORM do SQLAlchemy,
        # facilitando a conversão do modelo da base de dados (models.Usuario) para este schema.
        from_attributes = True

