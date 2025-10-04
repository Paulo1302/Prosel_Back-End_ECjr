from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.usuario_repository import UsuarioRepository 
from app.schemas.usuario import UsuarioCreate 
from app.core.security import get_password_hash, verify_password, create_access_token 


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UsuarioRepository()

    def register_user(self, user: UsuarioCreate):
        if self.repo.get_by_username(self.db, user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username já cadastrado."
            )
        hashed_password = get_password_hash(user.password)
        return self.repo.create(self.db, user, hashed_password)
    
    def login_for_access_token(self, form_data):
        user = self.repo.get_by_username(self.db, form_data.username)
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}