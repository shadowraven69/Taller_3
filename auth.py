import os
from datetime import datetime, timedelta
from typing import Optional, List
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.orm import Session
import models, schemas, database

SECRET_KEY = os.getenv("SECRET_KEY", "clave_por_defecto")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token",
    scopes={
        "tickets:crear": "Crear nuevos tickets",
        "tickets:ver_propios": "Ver los tickets propios",
        "tickets:recibir": "Cambiar estado de solicitado a recibido",
        "tickets:asignar": "Asignar ticket a un auxiliar o tecnico",
        "tickets:atender": "Cambiar estado a en_proceso o en_revision",
        "tickets:finalizar": "Cambiar estado a terminado",
        "tickets:ver_todos": "Ver todos los tickets del sistema",
        "usuarios:gestionar": "Crear, listar y consultar usuarios"
    }
)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

ROLES_SCOPES = {
    "solicitante": ["tickets:crear", "tickets:ver_propios"],
    "responsable_tecnico": ["tickets:ver_propios", "tickets:recibir", "tickets:asignar", "tickets:finalizar"],
    "auxiliar": ["tickets:ver_propios", "tickets:atender"],
    "tecnico_especializado": ["tickets:ver_propios", "tickets:atender"],
    "admin": ["tickets:crear", "tickets:ver_propios", "tickets:recibir", "tickets:asignar", "tickets:atender", "tickets:finalizar", "tickets:ver_todos", "usuarios:gestionar"]
}

def get_scopes_for_role(rol: str):
    return ROLES_SCOPES.get(rol, [])

def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
        
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": authenticate_value},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo: str = payload.get("sub")
        if correo is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = schemas.TokenData(scopes=token_scopes, correo=correo)
    except JWTError:
        raise credentials_exception
        
    user = db.query(models.Usuario).filter(models.Usuario.correo == token_data.correo).first()
    if user is None:
        raise credentials_exception
        
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permisos insuficientes",
                headers={"WWW-Authenticate": authenticate_value},
            )
            
    return user