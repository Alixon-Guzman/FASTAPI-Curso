from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.schemas.database import Base
import datetime


class RecursoTipoB(Base):
    __tablename__ = "recursos_tipo_b"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    capacidad = Column(Integer, nullable=False, default=1)

    reservas = relationship("ReservaTipoB", back_populates="recurso")


class ReservaTipoB(Base):
    __tablename__ = "reservas_tipo_b"

    id = Column(Integer, primary_key=True, index=True)
    recurso_id = Column(Integer, ForeignKey("recursos_tipo_b.id"))
    usuario = Column(String, nullable=False)
    fecha_inicio = Column(DateTime, default=datetime.datetime.utcnow)
    fecha_fin = Column(DateTime, nullable=False)

    recurso = relationship("RecursoTipoB", back_populates="reservas")
