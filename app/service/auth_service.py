# Importa o objeto Session do SQLAlchemy para tipagem.
from sqlalchemy.orm import Session
# Importa componentes do FastAPI para tratamento de erros HTTP.
from fastapi import HTTPException, status
# Importa o repositório de utilizador para aceder à base de dados.
from app.repositories.usuario_repository import UsuarioRepository 
# Importa o schema Pydantic para validação dos dados de entrada do utilizador.
from app.schemas.usuario import UsuarioCreate 
# Importa as funções de segurança para hashing de senhas e criação de tokens JWT.
from app.core.security import get_password_hash, verify_password, create_access_token 


class AuthService:
    """
    Camada de Serviço (Service Layer) para a lógica de negócio de autenticação.
    Esta classe orquestra as operações de registo e login, utilizando o repositório
    para interagir com a base de dados e as funções de segurança para manipular senhas e tokens.
    """

    def __init__(self, db: Session):
        """
        O construtor recebe a sessão da base de dados para ser usada em todos os métodos.
        :param db: A sessão da base de dados injetada pela dependência do FastAPI.
        """
        self.db = db
        self.repo = UsuarioRepository()

    def register_user(self, user: UsuarioCreate):
        """
        Executa a lógica de negócio para registar um novo utilizador.
        1. Verifica se o nome de utilizador já existe.
        2. Gera o hash da senha.
        3. Chama o repositório para criar o utilizador na base de dados.
        
        :param user: Um objeto Pydantic UsuarioCreate com os dados do novo utilizador.
        :return: O objeto ORM do utilizador recém-criado.
        """
        # Regra de negócio: Impede o registo de nomes de utilizador duplicados.
        if self.repo.get_by_username(self.db, user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nome de utilizador já registado."
            )
        # Gera o hash da senha antes de a armazenar.
        hashed_password = get_password_hash(user.password)
        # Delega a criação do utilizador à camada de repositório.
        return self.repo.create(self.db, user, hashed_password)
    
    def login_for_access_token(self, form_data):
        """
        Executa a lógica de negócio para autenticar um utilizador e gerar um token.
        1. Obtém o utilizador pelo nome de utilizador.
        2. Verifica se a senha fornecida corresponde à senha hasheada.
        3. Cria um token de acesso JWT se as credenciais forem válidas.
        
        :param form_data: Um objeto OAuth2PasswordRequestForm com 'username' e 'password'.
        :return: Um dicionário contendo o token de acesso e o tipo de token.
        """
        user = self.repo.get_by_username(self.db, form_data.username)
        
        # Regra de negócio: Verifica se o utilizador existe e se a senha está correta.
        # A verificação é feita em tempo constante para mitigar ataques de timing.
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Nome de utilizador ou senha incorretos",
                # O cabeçalho WWW-Authenticate é parte do padrão OAuth2 e informa o cliente
                # sobre o esquema de autenticação a ser usado.
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Cria o token de acesso, incluindo o nome de utilizador no "subject" (sub) do payload.
        access_token = create_access_token(data={"sub": user.username})
        
        # Retorna o token no formato esperado pelo padrão OAuth2.
        return {"access_token": access_token, "token_type": "bearer"}

