from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db 
from app.schemas import empresa as empresa_schema, usuario as usuario_schema 
from app.service.empresa_service import EmpresaService 
from app.repositories.empresa_repository import EmpresaRepository 
from app.deps import get_current_active_user 


router = APIRouter(
    prefix="/empresas",
    tags=["Empresas"],
    dependencies=[Depends(get_current_active_user)]
)

@router.post("/", response_model=empresa_schema.Empresa, status_code=status.HTTP_201_CREATED)
def create_empresa(empresa: empresa_schema.EmpresaCreate, db: Session = Depends(get_db)):
    service = EmpresaService(db)
    return service.create_empresa(empresa)

@router.get("/", response_model=List[empresa_schema.Empresa])
def list_empresas(
    cidade: Optional[str] = None, 
    ramo_atuacao: Optional[str] = None,
    nome: Optional[str] = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    filtros = {"cidade": cidade, "ramo_atuacao": ramo_atuacao, "nome": nome}
    repo = EmpresaRepository()
    return repo.get_all(db, skip, limit, filtros)

@router.get("/{empresa_id}", response_model=empresa_schema.Empresa)
def read_empresa(empresa_id: int, db: Session = Depends(get_db)):
    repo = EmpresaRepository()
    db_empresa = repo.get_by_id(db, empresa_id)
    if db_empresa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada.")
    return db_empresa

@router.put("/{empresa_id}", response_model=empresa_schema.Empresa)
def update_empresa(empresa_id: int, empresa: empresa_schema.EmpresaUpdate, db: Session = Depends(get_db)):
    service = EmpresaService(db)
    updated_empresa = service.update_empresa(empresa_id, empresa)
    return updated_empresa

@router.delete("/{empresa_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_empresa(empresa_id: int, db: Session = Depends(get_db)):
    repo = EmpresaRepository()
    if not repo.delete(db, empresa_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada.")
    return