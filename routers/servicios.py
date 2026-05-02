from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
import models, schemas, database, auth

router = APIRouter(
    prefix="/servicios",
    tags=["servicios"]
)

@router.post("/", response_model=schemas.ServicioResponse)
def crear_servicio(
    servicio: schemas.ServicioCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Security(auth.get_current_user)
):
    nuevo_servicio = models.Servicio(**servicio.dict())
    db.add(nuevo_servicio)
    db.commit()
    db.refresh(nuevo_servicio)
    return nuevo_servicio

@router.get("/", response_model=list[schemas.ServicioResponse])
def listar_servicios(
    skip: int = 0, limit: int = 100, 
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Security(auth.get_current_user)
):
    return db.query(models.Servicio).offset(skip).limit(limit).all()

@router.get("/{id_servicio}", response_model=schemas.ServicioResponse)
def obtener_servicio(
    id_servicio: int, 
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Security(auth.get_current_user)
):
    servicio = db.query(models.Servicio).filter(models.Servicio.id_servicio == id_servicio).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio