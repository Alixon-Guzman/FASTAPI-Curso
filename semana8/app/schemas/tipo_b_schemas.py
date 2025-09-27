from pydantic import BaseModel, Field
from datetime import datetime


class RecursoTipoBBase(BaseModel):
    nombre: str = Field(..., example="Camión de carga")
    descripcion: str | None = Field(None, example="Camión con capacidad de 5 toneladas")
    capacidad: int = Field(..., example=3)


class RecursoTipoBCreate(RecursoTipoBBase):
    pass


class RecursoTipoB(RecursoTipoBBase):
    id: int

    class Config:
        orm_mode = True


class ReservaTipoBBase(BaseModel):
    usuario: str = Field(..., example="cliente123")
    fecha_inicio: datetime = Field(..., example="2025-10-01T08:00:00")
    fecha_fin: datetime = Field(..., example="2025-10-01T12:00:00")


class ReservaTipoBCreate(ReservaTipoBBase):
    recurso_id: int = Field(..., example=1)


class ReservaTipoB(ReservaTipoBBase):
    id: int
    recurso_id: int

    class Config:
        orm_mode = True
