from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
import models, schemas, database, auth

router = APIRouter(
    prefix="/laboratorios",
    tags=["laboratorios"]
)

@router.post("/", response_model=schemas.LaboratorioResponse)
def crear_laboratorio(
    lab: schemas.LaboratorioCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Security(auth.get_current_user)
):
    nuevo_lab = models.Laboratorio(**lab.dict())
    db.add(nuevo_lab)
    db.commit()
    db.refresh(nuevo_lab)
    return nuevo_lab

@router.get("/", response_model=list[schemas.LaboratorioResponse])
def listar_laboratorios(
    skip: int = 0, limit: int = 100, 
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Security(auth.get_current_user)
):
    return db.query(models.Laboratorio).offset(skip).limit(limit).all()

@router.get("/{id_laboratorio}", response_model=schemas.LaboratorioResponse)
def obtener_laboratorio(
    id_laboratorio: int, 
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Security(auth.get_current_user)
):
    lab = db.query(models.Laboratorio).filter(models.Laboratorio.id_laboratorio == id_laboratorio).first()
    if not lab:
        raise HTTPException(status_code=404, detail="Laboratorio no encontrado")
    return lab