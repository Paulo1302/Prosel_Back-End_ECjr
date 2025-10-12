# Importa o objeto Session do SQLAlchemy para tipagem.
from sqlalchemy.orm import Session
# Importa componentes do FastAPI para tratamento de erros HTTP.
from fastapi import HTTPException, status
# Importa o repositório de empresa para aceder à base de dados.
from app.repositories.empresa_repository import EmpresaRepository 
# Importa os schemas Pydantic para validação dos dados de entrada.
from app.schemas import empresa as empresa_schema 


class EmpresaService:
    """
    Camada de Serviço (Service Layer) para a lógica de negócio da entidade Empresa.
    Esta classe orquestra as operações de criação e atualização, aplicando as regras
    de negócio antes de delegar as operações de persistência à camada de repositório.
    """

    def __init__(self, db: Session):
        """
        O construtor recebe a sessão da base de dados para ser usada em todos os métodos.
        :param db: A sessão da base de dados injetada pela dependência do FastAPI.
        """
        self.db = db
        self.repo = EmpresaRepository()

    def create_empresa(self, empresa: empresa_schema.EmpresaCreate):
        """
        Executa a lógica de negócio para criar uma nova empresa.
        1. Verifica se o CNPJ já existe.
        2. Verifica se o E-mail de contacto já existe.
        3. Se as validações passarem, chama o repositório para criar a empresa.
        
        :param empresa: Um objeto Pydantic EmpresaCreate com os dados da nova empresa.
        :return: O objeto ORM da empresa recém-criada.
        """
        # Regra de negócio: Impede o registo de CNPJs duplicados.
        if self.repo.get_by_cnpj(self.db, empresa.cnpj):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CNPJ já registado.")
        
        # Regra de negócio: Impede o registo de e-mails de contacto duplicados.
        if self.repo.get_by_email(self.db, empresa.email_contato):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail já registado.")
        
        # Delega a criação da empresa à camada de repositório.
        return self.repo.create(self.db, empresa)

    def update_empresa(self, empresa_id: int, empresa_update: empresa_schema.EmpresaUpdate):
        """
        Executa a lógica de negócio para atualizar uma empresa existente.
        1. Verifica se a empresa existe.
        2. Se um novo e-mail for fornecido, verifica se ele já está em uso por outra empresa.
        3. Se as validações passarem, chama o repositório para atualizar os dados.
        
        :param empresa_id: O ID da empresa a ser atualizada.
        :param empresa_update: Um objeto Pydantic EmpresaUpdate com os novos dados.
        :return: O objeto ORM da empresa atualizada.
        """
        db_empresa = self.repo.get_by_id(self.db, empresa_id)
        if not db_empresa:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada.")
        
        # Regra de negócio: Se o e-mail estiver a ser atualizado,
        # verifica se o novo e-mail já pertence a outra empresa.
        if empresa_update.email_contato:
            empresa_existente = self.repo.get_by_email(self.db, empresa_update.email_contato)
            if empresa_existente and empresa_existente.id != empresa_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail já registado noutra empresa.")
        
        # Delega a atualização à camada de repositório.
        return self.repo.update(self.db, empresa_id, empresa_update)

