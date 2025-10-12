# Importa o objeto Session do SQLAlchemy para tipagem e o motor de ORM.
from sqlalchemy.orm import Session
# Importa os módulos internos: 'models' para os ORMs e 'empresa_schema' para os modelos Pydantic.
from app.db import models 
from app.schemas import empresa as empresa_schema 
# Importa tipos do Python para type hinting, melhorando a legibilidade e a verificação estática.
from typing import Optional, List


class EmpresaRepository:
    """
    Camada de Acesso a Dados (Repository) para a entidade Empresa.
    Esta classe encapsula toda a lógica de interação direta com a base de dados
    para as operações de CRUD relacionadas com empresas.
    """

    def create(self, db: Session, empresa: empresa_schema.EmpresaCreate) -> models.Empresa:
        """
        Cria um novo registo de empresa na base de dados.
        :param db: A sessão da base de dados.
        :param empresa: Um objeto Pydantic EmpresaCreate com os dados da nova empresa.
        :return: O objeto ORM da empresa recém-criada.
        """
        # Desempacota o dicionário do modelo Pydantic para criar uma instância do modelo ORM.
        db_empresa = models.Empresa(**empresa.dict())
        db.add(db_empresa)  # Adiciona o novo objeto à sessão.
        db.commit()         # Persiste a transação na base de dados.
        db.refresh(db_empresa) # Atualiza o objeto com os dados da BD (ex: ID gerado).
        return db_empresa

    def get_by_id(self, db: Session, empresa_id: int) -> Optional[models.Empresa]:
        """
        Obtém um registo de empresa pelo seu ID.
        :param db: A sessão da base de dados.
        :param empresa_id: O ID da empresa a ser procurada.
        :return: O objeto ORM da empresa ou None se não for encontrado.
        """
        return db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()

    def get_by_cnpj(self, db: Session, cnpj: str) -> Optional[models.Empresa]:
        """Obtém um registo de empresa pelo seu CNPJ."""
        return db.query(models.Empresa).filter(models.Empresa.cnpj == cnpj).first()

    def get_by_email(self, db: Session, email: str) -> Optional[models.Empresa]:
        """Obtém um registo de empresa pelo seu email de contacto."""
        return db.query(models.Empresa).filter(models.Empresa.email_contato == email).first()

    def get_all(self, db: Session, skip: int, limit: int, filtros: dict) -> List[models.Empresa]:
        """
        Obtém uma lista de empresas, com suporte a paginação e filtros dinâmicos.
        :param db: A sessão da base de dados.
        :param skip: Número de registos a saltar (offset).
        :param limit: Número máximo de registos a retornar.
        :param filtros: Um dicionário contendo os filtros a serem aplicados (cidade, ramo, nome).
        :return: Uma lista de objetos ORM de empresas.
        """
        query = db.query(models.Empresa)
        # Aplica filtros dinamicamente se eles forem fornecidos.
        # .ilike() realiza uma correspondência de string insensível a maiúsculas/minúsculas.
        if filtros.get("cidade"):
            query = query.filter(models.Empresa.cidade.ilike(f"%{filtros['cidade']}%"))
        if filtros.get("ramo_atuacao"):
            query = query.filter(models.Empresa.ramo_atuacao.ilike(f"%{filtros['ramo_atuacao']}%"))
        if filtros.get("nome"):
            query = query.filter(models.Empresa.nome.ilike(f"%{filtros['nome']}%"))
        # Aplica a paginação e executa a consulta.
        return query.offset(skip).limit(limit).all()

    def update(self, db: Session, empresa_id: int, update_data: empresa_schema.EmpresaUpdate) -> Optional[models.Empresa]:
        """
        Atualiza os dados de um registo de empresa existente.
        :param db: A sessão da base de dados.
        :param empresa_id: O ID da empresa a ser atualizada.
        :param update_data: Um objeto Pydantic EmpresaUpdate com os novos dados.
        :return: O objeto ORM da empresa atualizada ou None se não for encontrada.
        """
        db_empresa = self.get_by_id(db, empresa_id)
        if db_empresa:
            # Itera sobre os dados fornecidos e atualiza os atributos do objeto ORM.
            # exclude_unset=True garante que apenas os campos explicitamente enviados sejam atualizados.
            for key, value in update_data.dict(exclude_unset=True).items():
                setattr(db_empresa, key, value)
            db.commit()
            db.refresh(db_empresa)
        return db_empresa

    def delete(self, db: Session, empresa_id: int) -> bool:
        """
        Apaga um registo de empresa da base de dados.
        :param db: A sessão da base de dados.
        :param empresa_id: O ID da empresa a ser apagada.
        :return: True se a empresa foi apagada com sucesso, False caso contrário.
        """
        db_empresa = self.get_by_id(db, empresa_id)
        if db_empresa:
            db.delete(db_empresa)
            db.commit()
            return True
        return False
