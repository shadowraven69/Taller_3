from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    rol: str
    activo: Optional[bool] = True

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioResponse(UsuarioBase):
    id_usuario: int

    class Config:
        from_attributes = True

class LaboratorioBase(BaseModel):
    nombre: str
    ubicacion: str
    activo: Optional[bool] = True

class LaboratorioCreate(LaboratorioBase):
    pass

class LaboratorioResponse(LaboratorioBase):
    id_laboratorio: int

    class Config:
        from_attributes = True

class ServicioBase(BaseModel):
    nombre: str
    descripcion: str
    activo: Optional[bool] = True

class ServicioCreate(ServicioBase):
    pass

class ServicioResponse(ServicioBase):
    id_servicio: int

    class Config:
        from_attributes = True

class TicketBase(BaseModel):
    id_laboratorio: int
    id_servicio: int
    titulo: str
    descripcion: str
    prioridad: str

class TicketCreate(TicketBase):
    pass

class TicketUpdateEstado(BaseModel):
    estado: str
    observacion_responsable: Optional[str] = None
    observacion_tecnico: Optional[str] = None
    id_asignado: Optional[int] = None

class TicketResponse(TicketBase):
    id_ticket: int
    id_solicitante: int
    id_responsable: Optional[int]
    id_asignado: Optional[int]
    estado: str
    observacion_responsable: Optional[str]
    observacion_tecnico: Optional[str]
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    fecha_finalizacion: Optional[datetime]

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    correo: Optional[str] = None
    scopes: List[str] = []