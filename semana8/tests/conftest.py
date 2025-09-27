import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.schemas.database import Base, get_db

# Base de datos de prueba (SQLite en memoria)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_fastmove.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Fixture: sesión de base de datos de prueba
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


# Fixture: cliente de pruebas que usa la DB de test
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


# Fixture: recurso de ejemplo Tipo B
@pytest.fixture
def sample_recurso_tipo_b(db_session):
    from app.models.tipo_b_models import RecursoTipoB

    recurso = RecursoTipoB(nombre="Camión 1", descripcion="Camión 5 toneladas", capacidad=2)
    db_session.add(recurso)
    db_session.commit()
    db_session.refresh(recurso)
    return recurso


# Fixture: reserva de ejemplo Tipo B
@pytest.fixture
def sample_reserva_tipo_b(db_session, sample_recurso_tipo_b):
    from app.models.tipo_b_models import ReservaTipoB
    import datetime

    reserva = ReservaTipoB(
        recurso_id=sample_recurso_tipo_b.id,
        usuario="cliente123",
        fecha_inicio=datetime.datetime(2025, 10, 1, 8, 0, 0),
        fecha_fin=datetime.datetime(2025, 10, 1, 12, 0, 0),
    )
    db_session.add(reserva)
    db_session.commit()
    db_session.refresh(reserva)
    return reserva
