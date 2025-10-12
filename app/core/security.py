# Importações necessárias para manipulação de datas, tipos, JWT e hashing.
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

# Importa a instância de configurações para aceder a segredos como a SECRET_KEY.
from .config import settings

# Configura o contexto do Passlib para hashing de senhas.
# - 'schemes=["bcrypt"]': Define o bcrypt como o algoritmo de hashing padrão e preferencial.
#   O bcrypt é uma escolha robusta e padrão da indústria para hashing de senhas devido à sua lentidão
#   e uso de um "salt" para proteger contra ataques de rainbow table.
# - 'deprecated="auto"': Permite que o Passlib verifique senhas com hashes mais antigos (se aplicável)
#   e os atualize automaticamente para o esquema preferencial (bcrypt) se a verificação for bem-sucedida.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde a uma senha com hash.
    
    :param plain_password: A senha fornecida pelo utilizador durante o login.
    :param hashed_password: A senha com hash armazenada na base de dados.
    :return: True se as senhas corresponderem, False caso contrário.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Gera o hash de uma senha em texto plano usando o esquema padrão (bcrypt).
    
    :param password: A senha a ser hasheada.
    :return: A representação da senha em hash.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um novo token de acesso JWT.
    
    :param data: Um dicionário de dados a serem incluídos no "payload" do token (o "claim").
                 Normalmente contém o identificador do utilizador (ex: {"sub": username}).
    :param expires_delta: Um objeto timedelta opcional para definir um tempo de expiração personalizado.
    :return: O token JWT codificado como uma string.
    """
    to_encode = data.copy()
    
    # Define o tempo de expiração do token.
    # Se um 'expires_delta' for fornecido, usa-o.
    # Caso contrário, usa o valor padrão definido nas configurações.
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Adiciona a data de expiração ("exp" claim) ao payload do token.
    # O 'exp' é um claim registado pelo padrão JWT e é crucial para a segurança.
    to_encode.update({"exp": expire})
    
    # Codifica o payload para criar o JWT final.
    # Usa a SECRET_KEY e o ALGORITHM definidos nas configurações para assinar o token.
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt

