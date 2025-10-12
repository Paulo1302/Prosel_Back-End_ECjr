# Importações necessárias do FastAPI, bibliotecas de segurança e módulos do projeto.
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

# Importações de módulos internos da aplicação.
from app.core.config import settings 
from app.db.database import get_db 
from app.schemas.token import TokenData 
from app.repositories.usuario_repository import UsuarioRepository 

# Configura o esquema de segurança OAuth2.
# O FastAPI usará isto para identificar como o token deve ser fornecido.
# "tokenUrl" indica ao Swagger UI qual endpoint deve ser usado para obter o token (o de login).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_active_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dependência do FastAPI para validar o token JWT e obter o utilizador atual.
    
    Esta função é usada para proteger os endpoints. Ela executa antes de cada pedido
    a uma rota protegida e faz o seguinte:
    1. Exige um token no cabeçalho Authorization.
    2. Decodifica e valida o token.
    3. Procura o utilizador correspondente na base de dados.
    
    Se qualquer passo falhar, levanta uma exceção HTTPException, bloqueando o acesso.
    Se for bem-sucedida, retorna o objeto do utilizador autenticado.
    """
    
    # Define uma exceção padrão a ser retornada se a autenticação falhar.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Tenta decodificar o token usando a chave secreta e o algoritmo definidos.
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # Extrai o nome de utilizador ("subject") do payload do token.
        username: str = payload.get("sub")
        if username is None:
            # Se não houver nome de utilizador no token, levanta a exceção.
            raise credentials_exception
        
        # Valida os dados do token com o schema Pydantic.
        token_data = TokenData(username=username)
    except JWTError:
        # Se ocorrer um erro durante a decodificação (token inválido, expirado, etc.),
        # levanta a exceção.
        raise credentials_exception
    
    # Cria uma instância do repositório para aceder à base de dados.
    repo = UsuarioRepository()
    
    # Procura o utilizador na base de dados pelo nome de utilizador extraído do token.
    user = repo.get_by_username(db, username=token_data.username)
    if user is None:
        # Se o utilizador não for encontrado na base de dados, levanta a exceção.
        # Isto protege contra tokens válidos de utilizadores que foram entretanto apagados.
        raise credentials_exception
        
    # Se tudo estiver correto, retorna o objeto do utilizador.
    # Este utilizador pode ser injetado nos endpoints que usam esta dependência.
    return user