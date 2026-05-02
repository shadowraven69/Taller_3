from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.orm import Session
import models, schemas, database, auth

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"]
)

@router.post("/", response_model=schemas.TicketResponse)
def crear_ticket(
    ticket: schemas.TicketCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Security(auth.get_current_user, scopes=["tickets:crear"])
):
    nuevo_ticket = models.Ticket(**ticket.dict(), id_solicitante=current_user.id_usuario)
    db.add(nuevo_ticket)
    db.commit()
    db.refresh(nuevo_ticket)
    return nuevo_ticket

@router.get("/", response_model=list[schemas.TicketResponse])
def listar_tickets(
    skip: int = 0, limit: int = 100, 
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Security(auth.get_current_user, scopes=["tickets:ver_propios"])
):
    query = db.query(models.Ticket)
    
    if current_user.rol == "admin":
        return query.offset(skip).limit(limit).all()
        
    elif current_user.rol == "solicitante":
        return query.filter(models.Ticket.id_solicitante == current_user.id_usuario).offset(skip).limit(limit).all()
        
    elif current_user.rol == "responsable_tecnico":
        return query.filter(
            (models.Ticket.id_responsable == current_user.id_usuario) |
            (models.Ticket.id_solicitante == current_user.id_usuario) |
            (models.Ticket.estado == "solicitado") # Puede ver los solicitados para recibirlos
        ).offset(skip).limit(limit).all()
        
    elif current_user.rol in ["auxiliar", "tecnico_especializado"]:
        return query.filter(
            (models.Ticket.id_asignado == current_user.id_usuario) |
            (models.Ticket.id_solicitante == current_user.id_usuario)
        ).offset(skip).limit(limit).all()
        
    return []

@router.get("/{id_ticket}", response_model=schemas.TicketResponse)
def obtener_ticket(
    id_ticket: int, 
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Security(auth.get_current_user, scopes=["tickets:ver_propios"])
):
    ticket = db.query(models.Ticket).filter(models.Ticket.id_ticket == id_ticket).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
        
    if current_user.rol == "solicitante" and ticket.id_solicitante != current_user.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes acceso a este ticket")
    if current_user.rol in ["auxiliar", "tecnico_especializado"]:
        if ticket.id_solicitante != current_user.id_usuario and ticket.id_asignado != current_user.id_usuario:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes acceso a este ticket")
            
    return ticket

@router.patch("/{id_ticket}/estado", response_model=schemas.TicketResponse)
def actualizar_estado_ticket(
    id_ticket: int, 
    ticket_update: schemas.TicketUpdateEstado, 
    db: Session = Depends(database.get_db),
    # Requiere uno de estos scopes (validado manualmente)
    current_user: models.Usuario = Security(auth.get_current_user)
):
    ticket = db.query(models.Ticket).filter(models.Ticket.id_ticket == id_ticket).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    estado_actual = ticket.estado
    estado_nuevo = ticket_update.estado
    
    if estado_actual == "solicitado" and estado_nuevo == "recibido":
        if "tickets:recibir" not in auth.get_scopes_for_role(current_user.rol):
            raise HTTPException(status_code=403, detail="No tienes permisos para recibir tickets")
        ticket.id_responsable = current_user.id_usuario

    elif estado_actual == "recibido" and estado_nuevo == "asignado":
        if "tickets:asignar" not in auth.get_scopes_for_role(current_user.rol):
            raise HTTPException(status_code=403, detail="No tienes permisos para asignar tickets")
        if not ticket_update.id_asignado:
            raise HTTPException(status_code=422, detail="Debe especificar id_asignado")
        ticket.id_asignado = ticket_update.id_asignado

    elif estado_actual == "asignado" and estado_nuevo == "en_proceso":
        if "tickets:atender" not in auth.get_scopes_for_role(current_user.rol):
            raise HTTPException(status_code=403, detail="No tienes permisos para atender tickets")
        if current_user.rol != "admin" and ticket.id_asignado != current_user.id_usuario:
            raise HTTPException(status_code=403, detail="Solo el tecnico asignado puede procesar este ticket")

    elif estado_actual == "en_proceso" and estado_nuevo == "en_revision":
        if "tickets:atender" not in auth.get_scopes_for_role(current_user.rol):
            raise HTTPException(status_code=403, detail="No tienes permisos para atender tickets")
        if current_user.rol != "admin" and ticket.id_asignado != current_user.id_usuario:
            raise HTTPException(status_code=403, detail="Solo el tecnico asignado puede enviar a revision este ticket")
        if ticket_update.observacion_tecnico:
            ticket.observacion_tecnico = ticket_update.observacion_tecnico

    elif estado_actual == "en_revision" and estado_nuevo == "terminado":
        if "tickets:finalizar" not in auth.get_scopes_for_role(current_user.rol):
            raise HTTPException(status_code=403, detail="No tienes permisos para finalizar tickets")
        if ticket_update.observacion_responsable:
            ticket.observacion_responsable = ticket_update.observacion_responsable
        from datetime import datetime
        ticket.fecha_finalizacion = datetime.utcnow()

    else:
        raise HTTPException(status_code=422, detail=f"Transicion de estado no permitida: {estado_actual} a {estado_nuevo}")

    ticket.estado = estado_nuevo
    db.commit()
    db.refresh(ticket)
    return ticket
