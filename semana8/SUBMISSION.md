# Entrega Semana 8 - Ficha 3147246

## Información del estudiante
- **Nombre:** GUZMAN GARZON  
- **Ficha:** 3147246  
- **Dominio asignado:** Empresa Logística FastMove (Tipo B: Programación temporal + Testing de API)  

---

## 📂 Entregables

### ✅ Práctica 27 – Pytest Básico
- Configuración de `tests/conftest.py` con fixtures (`db_session`, `client`, `sample_recurso_tipo_b`, `sample_reserva_tipo_b`).
- Archivo `configs/pytest.ini` con coverage mínimo de 80%.
- Pruebas unitarias en `tests/test_tipo_b/test_models.py`.
- Pruebas de endpoints iniciales en `tests/test_tipo_b/test_endpoints.py`.

### ✅ Práctica 28 – API Testing
- Fixtures avanzadas (`authenticated_client`, `client_with_db_rollback`).
- Pruebas de integración CRUD completas en `tests/test_tipo_b/test_endpoints.py`.
- Validación de errores (400, 401, 404).
- Ejecución de `pytest` con coverage > 80%.

### ✅ Práctica 29 – Documentación Avanzada
- Archivo `app/docs/descriptions.py` con `API_DESCRIPTION` y `TAGS_METADATA`.
- Endpoints documentados con `summary`, `tags` y `response_model`.
- Uso de `json_schema_extra` en Pydantic schemas.
- Documentación interactiva accesible en:
  - `/docs` (Swagger UI)
  - `/redoc` (ReDoc)

### ✅ Práctica 30 – Code Quality & CI
- Archivo `configs/pyproject.toml` con configuraciones de Black, isort, Flake8, MyPy y Bandit.
- Archivo `configs/.pre-commit-config.yaml` con hooks configurados.
- Scripts en `scripts/format.sh`, `scripts/lint.sh`, `scripts/quality.sh`.
- Workflow `.github/workflows/ci.yml` para integración continua.
- Reporte de coverage (`htmlcov/index.html`) generado con pytest.

---

## 📊 Resultados de pruebas

- Comando usado:
  ```bash
  pytest --cov=app --cov-report=term-missing
