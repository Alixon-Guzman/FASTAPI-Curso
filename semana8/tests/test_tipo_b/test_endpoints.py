import datetime


def test_crear_recurso(client):
    response = client.post(
        "/api/tipo-b/recursos",
        json={"nombre": "Montacargas", "descripcion": "Montacargas eléctrico", "capacidad": 5},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Montacargas"
    assert data["capacidad"] == 5


def test_obtener_recurso(client, sample_recurso_tipo_b):
    response = client.get(f"/api/tipo-b/recursos/{sample_recurso_tipo_b.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Camión 1"


def test_crear_reserva_sin_conflicto(client, sample_recurso_tipo_b):
    body = {
        "usuario": "clienteABC",
        "fecha_inicio": "2025-10-02T08:00:00",
        "fecha_fin": "2025-10-02T12:00:00",
        "recurso_id": sample_recurso_tipo_b.id,
    }
    response = client.post("/api/tipo-b/reservas", json=body)
    assert response.status_code == 200
    data = response.json()
    assert data["usuario"] == "clienteABC"


def test_crear_reserva_con_conflicto(client, sample_reserva_tipo_b):
    body = {
        "usuario": "clienteXYZ",
        "fecha_inicio": "2025-10-01T09:00:00",  # Se solapa con sample_reserva
        "fecha_fin": "2025-10-01T11:00:00",
        "recurso_id": sample_reserva_tipo_b.recurso_id,
    }
    response = client.post("/api/tipo-b/reservas", json=body)
    assert response.status_code == 400
    assert response.json()["detail"] == "Conflicto de horario con otra reserva"
