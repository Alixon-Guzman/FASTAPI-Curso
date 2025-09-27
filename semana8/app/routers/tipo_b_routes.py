from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import tipo_b_schemas
from app.models import tipo_b_models
from app.auth.dependencies import get_db, get_current_user

router = APIRouter()


@router.post("/recursos", response_model=tipo_b_schemas.RecursoTipoB, summary="Crear un recurso")
def crear_recurso(recurso: tipo_b_schemas.RecursoTipoBCreate, db: Session = Depends(get_db)):
    nuevo_recurso = tipo_b_models.RecursoTipoB(**recurso.dict())
    db.add(nuevo_recurso)
    db.commit()
    db.refresh(nuevo_recurso)
    return nuevo_recurso


@router.get("/recursos/{recurso_id}", response_model=tipo_b_schemas.RecursoTipoB, summary="Obtener un recurso por ID")
def obtener_recurso(recurso_id: int, db: Session = Depends(get_db)):
    recurso = db.query(tipo_b_models.RecursoTipoB).filter(tipo_b_models.RecursoTipoB.id == recurso_id).first()
    if not recurso:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    return recurso


@router.post("/reservas", response_model=tipo_b_schemas.ReservaTipoB, summary="Crear una reserva")
def crear_reserva(
    reserva: tipo_b_schemas.ReservaTipoBCreate,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):
    # Validar que el recurso exista
    recurso = db.query(tipo_b_models.RecursoTipoB).filter(tipo_b_models.RecursoTipoB.id == reserva.recurso_id).first()
    if not recurso:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

    # Validar conflicto de horarios
    conflictos = (
        db.query(tipo_b_models.ReservaTipoB)
        .filter(
            tipo_b_models.ReservaTipoB.recurso_id == reserva.recurso_id,
            tipo_b_models.ReservaTipoB.fecha_inicio < reserva.fecha_fin,
            tipo_b_models.ReservaTipoB.fecha_fin > reserva.fecha_inicio,
        )
        .all()
    )
    if conflictos:
        raise HTTPException(status_code=400, detail="Conflicto de horario con otra reserva")

    nueva_reserva = tipo_b_models.ReservaTipoB(**reserva.dict(), usuario=user)
    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)
    return nueva_reserva
