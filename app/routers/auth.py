# Importa os componentes necessários do FastAPI, como o APIRouter para modularização,
# Depends para injeção de dependências, e status para códigos de estado HTTP.
from fastapi import APIRouter, Depends, status
# Importa OAuth2PasswordRequestForm, uma classe de dependência que extrai o username e a password
# de um pedido de formulário (form data), como especificado pelo OAuth2.
from fastapi.security import OAuth2PasswordRequestForm
# Importa o objeto Session do SQLAlchemy para tipagem.
from sqlalchemy.orm import Session

# Importa os módulos internos da aplicação.
from app.db.database import get_db
from app.schemas import usuario as usuario_schema, token as token_schema
from app.service.auth_service import AuthService

# Cria uma instância de APIRouter para agrupar os endpoints relacionados à autenticação.
# Isto ajuda a manter o ficheiro principal (main.py) limpo e a organizar o projeto por funcionalidades.
# 'tags' agrupa estes endpoints na documentação automática do Swagger UI.
router = APIRouter(tags=["Autenticação"])

@router.post("/register", response_model=usuario_schema.Usuario, status_code=status.HTTP_201_CREATED)
def register_user(user: usuario_schema.UsuarioCreate, db: Session = Depends(get_db)):
    """
    Endpoint para registar um novo utilizador administrador.
    
    - Recebe os dados do utilizador (username, password) validados pelo schema UsuarioCreate.
    - Delega a lógica de negócio (verificação de duplicados, hashing de senha, etc.)
      para a camada de serviço (AuthService).
    - Retorna os dados do utilizador criado (sem a senha) com o status 201 Created.
    """
    service = AuthService(db)
    return service.register_user(user)

@router.post("/login", response_model=token_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint para autenticar um utilizador e retornar um token de acesso JWT.
    
    - Utiliza a dependência OAuth2PasswordRequestForm para extrair 'username' e 'password'
      do corpo do pedido (enviado como form-data).
    - Delega a lógica de autenticação (verificação de credenciais e criação do token)
      para a camada de serviço (AuthService).
    - Retorna um objeto Token contendo o access_token e o token_type.
    """
    service = AuthService(db)
    return service.login_for_access_token(form_data)
