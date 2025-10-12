# Importações necessárias do FastAPI e do SQLAlchemy.
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# Importações para type hinting.
from typing import List, Optional

# Importações dos módulos internos da aplicação.
from app.db.database import get_db 
from app.schemas import empresa as empresa_schema, usuario as usuario_schema 
from app.service.empresa_service import EmpresaService 
from app.repositories.empresa_repository import EmpresaRepository 
from app.deps import get_current_active_user 

# Cria uma instância de APIRouter para agrupar os endpoints de gestão de empresas.
router = APIRouter(
    # 'prefix' adiciona "/empresas" ao início de todas as rotas definidas neste router.
    prefix="/empresas",
    # 'tags' agrupa estes endpoints na documentação automática do Swagger UI.
    tags=["Empresas"],
    # 'dependencies' aplica uma ou mais dependências a TODAS as rotas deste router.
    # Aqui, estamos a usar get_current_active_user para garantir que apenas utilizadores
    # autenticados possam aceder a qualquer endpoint de gestão de empresas.
    dependencies=[Depends(get_current_active_user)]
)

@router.post("/", response_model=empresa_schema.Empresa, status_code=status.HTTP_201_CREATED)
def create_empresa(empresa: empresa_schema.EmpresaCreate, db: Session = Depends(get_db)):
    """Endpoint para criar uma nova empresa."""
    service = EmpresaService(db)
    return service.create_empresa(empresa)

@router.get("/", response_model=List[empresa_schema.Empresa])
def list_empresas(
    # Parâmetros de consulta (query parameters) para filtragem, todos opcionais.
    cidade: Optional[str] = None, 
    ramo_atuacao: Optional[str] = None,
    nome: Optional[str] = None,
    # Parâmetros de consulta para paginação.
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Endpoint para listar empresas com suporte a filtros e paginação."""
    filtros = {"cidade": cidade, "ramo_atuacao": ramo_atuacao, "nome": nome}
    # A lógica de filtragem está no repositório, mantendo o endpoint limpo.
    repo = EmpresaRepository()
    return repo.get_all(db, skip, limit, filtros)

@router.get("/{empresa_id}", response_model=empresa_schema.Empresa)
def read_empresa(empresa_id: int, db: Session = Depends(get_db)):
    """Endpoint para obter os detalhes de uma empresa específica pelo seu ID."""
    repo = EmpresaRepository()
    db_empresa = repo.get_by_id(db, empresa_id)
    if db_empresa is None:
        # Se a empresa não for encontrada, retorna um erro 404 Not Found.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada.")
    return db_empresa

@router.put("/{empresa_id}", response_model=empresa_schema.Empresa)
def update_empresa(empresa_id: int, empresa: empresa_schema.EmpresaUpdate, db: Session = Depends(get_db)):
    """Endpoint para atualizar os dados de uma empresa existente."""
    service = EmpresaService(db)
    updated_empresa = service.update_empresa(empresa_id, empresa)
    return updated_empresa

@router.delete("/{empresa_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_empresa(empresa_id: int, db: Session = Depends(get_db)):
    """Endpoint para apagar uma empresa."""
    repo = EmpresaRepository()
    success = repo.delete(db, empresa_id)
    if not success:
        # Se o repositório retornar False, significa que a empresa não foi encontrada.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada.")
    # Em caso de sucesso, retorna uma resposta 204 No Content, sem corpo.
    return
