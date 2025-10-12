# Importa o objeto Session do SQLAlchemy para tipagem e o motor de ORM.
from sqlalchemy.orm import Session
# Importa os módulos internos: 'models' para os ORMs e 'usuario_schema' para os modelos Pydantic.
from app.db import models 
from app.schemas import usuario as usuario_schema 

class UsuarioRepository:
    """
    Camada de Acesso a Dados (Repository) para a entidade Usuario.
    Esta classe encapsula toda a lógica de interação direta com a base de dados
    para as operações relacionadas com utilizadores (administradores).
    """

    def get_by_username(self, db: Session, username: str) -> models.Usuario:
        """
        Obtém um registo de utilizador pelo seu nome de utilizador (username).
        Este método é fundamental para os processos de login e registo, para verificar
        se um utilizador existe.
        
        :param db: A sessão da base de dados.
        :param username: O nome de utilizador a ser procurado.
        :return: O objeto ORM do utilizador ou None se não for encontrado.
        """
        return db.query(models.Usuario).filter(models.Usuario.username == username).first()

    def create(self, db: Session, user: usuario_schema.UsuarioCreate, hashed_password: str) -> models.Usuario:
        """
        Cria um novo registo de utilizador na base de dados.
        
        :param db: A sessão da base de dados.
        :param user: Um objeto Pydantic UsuarioCreate com os dados do novo utilizador.
        :param hashed_password: A representação da senha do utilizador após passar pelo algoritmo de hashing.
        :return: O objeto ORM do utilizador recém-criado.
        """
        # Cria uma instância do modelo ORM Usuario, passando os dados validados.
        # A senha é armazenada na sua forma hasheada para segurança.
        db_user = models.Usuario(username=user.username, hashed_password=hashed_password)
        db.add(db_user)  # Adiciona o novo objeto à sessão.
        db.commit()         # Persiste a transação na base de dados.
        db.refresh(db_user) # Atualiza o objeto com os dados da BD (ex: ID gerado).
        return db_user
