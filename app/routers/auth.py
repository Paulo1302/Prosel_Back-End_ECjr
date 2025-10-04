from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..db.database import get_db
from app.schemas import usuario as usuario_schema, token as token_schema
from app.service.auth_service import AuthService

router = APIRouter(tags=["Autenticação"])

@router.post("/register", response_model=usuario_schema.Usuario, status_code=status.HTTP_201_CREATED)
def register_user(user: usuario_schema.UsuarioCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.register_user(user)

@router.post("/login", response_model=token_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login_for_access_token(form_data)