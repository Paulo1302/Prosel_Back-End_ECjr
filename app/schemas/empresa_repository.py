from sqlalchemy.orm import Session
from ..db import models
from ..schemas import empresa as empresa_schema
from typing import Optional, List

class EmpresaRepository:
    """Repositório para operações de CRUD com a entidade Empresa."""

    def create(self, db: Session, empresa: empresa_schema.EmpresaCreate) -> models.Empresa:
        db_empresa = models.Empresa(**empresa.dict())
        db.add(db_empresa)
        db.commit()
        db.refresh(db_empresa)
        return db_empresa

    def get_by_id(self, db: Session, empresa_id: int) -> Optional[models.Empresa]:
        return db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()

    def get_by_cnpj(self, db: Session, cnpj: str) -> Optional[models.Empresa]:
        return db.query(models.Empresa).filter(models.Empresa.cnpj == cnpj).first()

    def get_by_email(self, db: Session, email: str) -> Optional[models.Empresa]:
        return db.query(models.Empresa).filter(models.Empresa.email_contato == email).first()

    def get_all(self, db: Session, skip: int, limit: int, filtros: dict) -> List[models.Empresa]:
        query = db.query(models.Empresa)
        if filtros.get("cidade"):
            query = query.filter(models.Empresa.cidade.ilike(f"%{filtros['cidade']}%"))
        if filtros.get("ramo_atuacao"):
            query = query.filter(models.Empresa.ramo_atuacao.ilike(f"%{filtros['ramo_atuacao']}%"))
        if filtros.get("nome"):
            query = query.filter(models.Empresa.nome.ilike(f"%{filtros['nome']}%"))
        return query.offset(skip).limit(limit).all()

    def update(self, db: Session, empresa_id: int, update_data: empresa_schema.EmpresaUpdate) -> Optional[models.Empresa]:
        db_empresa = self.get_by_id(db, empresa_id)
        if db_empresa:
            for key, value in update_data.dict(exclude_unset=True).items():
                setattr(db_empresa, key, value)
            db.commit()
            db.refresh(db_empresa)
        return db_empresa

    def delete(self, db: Session, empresa_id: int) -> bool:
        db_empresa = self.get_by_id(db, empresa_id)
        if db_empresa:
            db.delete(db_empresa)
            db.commit()
            return True
        return False