from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.config import settings 
from app.db.database import get_db 
from app.schemas.token import TokenData 
from app.repositories.usuario_repository import UsuarioRepository 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_active_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    repo = UsuarioRepository()
    user = repo.get_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user