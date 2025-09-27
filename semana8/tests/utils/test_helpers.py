import datetime


def crear_recurso_payload(nombre="Recurso X", descripcion="Demo", capacidad=1):
    return {"nombre": nombre, "descripcion": descripcion, "capacidad": capacidad}


def crear_reserva_payload(recurso_id: int, usuario="demo_user"):
    return {
        "usuario": usuario,
        "fecha_inicio": (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat(),
        "fecha_fin": (datetime.datetime.utcnow() + datetime.timedelta(hours=2)).isoformat(),
        "recurso_id": recurso_id,
    }
