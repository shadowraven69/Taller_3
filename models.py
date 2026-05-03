from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    correo = Column(String, unique=True, index=True)
    password_hash = Column(String)
    rol = Column(String)
    activo = Column(Boolean, default=True)

    # Relaciones
    tickets_solicitados = relationship("Ticket", foreign_keys="[Ticket.id_solicitante]", back_populates="solicitante")
    tickets_responsable = relationship("Ticket", foreign_keys="[Ticket.id_responsable]", back_populates="responsable")
    tickets_asignados = relationship("Ticket", foreign_keys="[Ticket.id_asignado]", back_populates="asignado")


class Laboratorio(Base):
    __tablename__ = "laboratorios"

    id_laboratorio = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    ubicacion = Column(String)
    activo = Column(Boolean, default=True)

    tickets = relationship("Ticket", back_populates="laboratorio")


class Servicio(Base):
    __tablename__ = "servicios"

    id_servicio = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    activo = Column(Boolean, default=True)

    tickets = relationship("Ticket", back_populates="servicio")


class Ticket(Base):
    __tablename__ = "tickets"

    id_ticket = Column(Integer, primary_key=True, index=True)
    id_solicitante = Column(Integer, ForeignKey("usuarios.id_usuario"))
    id_laboratorio = Column(Integer, ForeignKey("laboratorios.id_laboratorio"))
    id_servicio = Column(Integer, ForeignKey("servicios.id_servicio"))
    id_responsable = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)
    id_asignado = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)
    
    titulo = Column(String)
    descripcion = Column(String)
    estado = Column(String, default="solicitado")
    prioridad = Column(String)
    observacion_responsable = Column(String, nullable=True)
    observacion_tecnico = Column(String, nullable=True)
    
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    fecha_finalizacion = Column(DateTime, nullable=True)

    # Relaciones
    solicitante = relationship("Usuario", foreign_keys=[id_solicitante], back_populates="tickets_solicitados")
    responsable = relationship("Usuario", foreign_keys=[id_responsable], back_populates="tickets_responsable")
    asignado = relationship("Usuario", foreign_keys=[id_asignado], back_populates="tickets_asignados")
    laboratorio = relationship("Laboratorio", back_populates="tickets")
    servicio = relationship("Servicio", back_populates="tickets")