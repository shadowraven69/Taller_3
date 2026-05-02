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