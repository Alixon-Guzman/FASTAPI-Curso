from app.models.tipo_b_models import RecursoTipoB, ReservaTipoB
import datetime


def test_create_recurso_tipo_b():
    recurso = RecursoTipoB(nombre="Bodega A", descripcion="Bodega central", capacidad=50)
    assert recurso.nombre == "Bodega A"
    assert recurso.capacidad == 50


def test_create_reserva_tipo_b():
    reserva = ReservaTipoB(
        recurso_id=1,
        usuario="clienteXYZ",
        fecha_inicio=datetime.datetime(2025, 10, 1, 10, 0),
        fecha_fin=datetime.datetime(2025, 10, 1, 12, 0),
    )
    assert reserva.usuario == "clienteXYZ"
    assert reserva.fecha_inicio < reserva.fecha_fin
