from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.empresa_repository import EmpresaRepository 
from app.schemas import empresa as empresa_schema 


class EmpresaService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = EmpresaRepository()

    def create_empresa(self, empresa: empresa_schema.EmpresaCreate):
        if self.repo.get_by_cnpj(self.db, empresa.cnpj):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CNPJ já cadastrado.")
        if self.repo.get_by_email(self.db, empresa.email_contato):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail já cadastrado.")
        
        return self.repo.create(self.db, empresa)

    def update_empresa(self, empresa_id: int, empresa_update: empresa_schema.EmpresaUpdate):
        db_empresa = self.repo.get_by_id(self.db, empresa_id)
        if not db_empresa:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada.")
        
        if empresa_update.email_contato:
            empresa_existente = self.repo.get_by_email(self.db, empresa_update.email_contato)
            if empresa_existente and empresa_existente.id != empresa_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail já cadastrado em outra empresa.")
        
        return self.repo.update(self.db, empresa_id, empresa_update)