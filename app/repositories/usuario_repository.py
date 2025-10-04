from sqlalchemy.orm import Session
from app.db import models 
from app.schemas import usuario as usuario_schema 

class UsuarioRepository:
    def get_by_username(self, db: Session, username: str):
        return db.query(models.Usuario).filter(models.Usuario.username == username).first()

    def create(self, db: Session, user: usuario_schema.UsuarioCreate, hashed_password: str):
        db_user = models.Usuario(username=user.username, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user