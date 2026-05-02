from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
import models, schemas, database, auth

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

@router.post("/", response_model=schemas.UsuarioResponse)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.Usuario).filter(models.Usuario.correo == usuario.correo).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El correo ya esta registrado")
    
    nuevo_usuario = models.Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        password_hash=auth.get_password_hash(usuario.password),
        rol=usuario.rol,
        activo=usuario.activo
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.get("/", response_model=list[schemas.UsuarioResponse])
def listar_usuarios(
    skip: int = 0, limit: int = 100, 
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Security(auth.get_current_user, scopes=["usuarios:gestionar"])
):
    usuarios = db.query(models.Usuario).offset(skip).limit(limit).all()
    return usuarios

@router.get("/{id_usuario}", response_model=schemas.UsuarioResponse)
def obtener_usuario(
    id_usuario: int, 
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Security(auth.get_current_user, scopes=["usuarios:gestionar"])
):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_usuario).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario
