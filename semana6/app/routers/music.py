from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from app.routers.auth import get_current_user

router = APIRouter()

class Clase(BaseModel):
    id: Optional[int] = None
    nombre: str
    profesor: str
    duracion_minutos: int
    nivel: str
    cupo_maximo: int
    horario: str
    precio: float

clases: List[dict] = []
contador = 1

@router.post("/clases/", status_code=201)
def crear_clase(clase: Clase, user=Depends(get_current_user)):
    global contador
    clase.id = contador
    contador += 1
    clases.append(clase.dict())
    return clase

@router.get("/clases/{clase_id}")
def obtener_clase(clase_id: int, user=Depends(get_current_user)):
    for c in clases:
        if c["id"] == clase_id:
            return c
    raise HTTPException(status_code=404, detail="Clase no encontrada")

@router.put("/clases/{clase_id}")
def actualizar_clase(clase_id: int, datos: dict, user=Depends(get_current_user)):
    for c in clases:
        if c["id"] == clase_id:
            c.update(datos)
            return c
    raise HTTPException(status_code=404, detail="Clase no encontrada")

@router.delete("/clases/{clase_id}")
def eliminar_clase(clase_id: int, user=Depends(get_current_user)):
    if user["role"] != "admin_academia":
        raise HTTPException(status_code=403, detail="Solo admin puede eliminar clases")
    for c in clases:
        if c["id"] == clase_id:
            clases.remove(c)
            return {"message": "Clase eliminada"}
    raise HTTPException(status_code=404, detail="Clase no encontrada")
