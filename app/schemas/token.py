# Importa o BaseModel do Pydantic, a classe base para todos os modelos de validação de dados.
from pydantic import BaseModel
# Importa o Optional do typing para indicar que um campo pode ou não estar presente.
from typing import Optional

class Token(BaseModel):
    """
    Schema Pydantic para a resposta do endpoint de login.
    Define a estrutura do JSON que é retornado ao cliente após uma autenticação bem-sucedida.
    """
    # O token de acesso JWT gerado que o cliente usará para autenticar pedidos futuros.
    access_token: str
    # O tipo do token. Pelo padrão OAuth2, é tipicamente "bearer".
    token_type: str

class TokenData(BaseModel):
    """
    Schema Pydantic para os dados contidos dentro do payload de um token JWT.
    É usado para validar o conteúdo do token após a sua descodificação para garantir
    que contém os "claims" esperados.
    """
    # O nome de utilizador ("subject" do token) que está associado ao token.
    # É definido como Optional porque o payload pode não conter este campo,
    # permitindo uma validação explícita no código.
    username: Optional[str] = None
