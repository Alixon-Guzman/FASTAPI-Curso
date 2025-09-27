# Variables
PYTHON = python
PIP = pip

# Instalación de dependencias
install:
	$(PIP) install -r requirements/base.txt
	$(PIP) install -r requirements/dev.txt
	$(PIP) install -r requirements/test.txt

# Formateo automático con Black e isort
format:
	bash scripts/format.sh

# Linter con Flake8
lint:
	bash scripts/lint.sh

# Verificación de calidad completa (Black, isort, Flake8, MyPy, Bandit, Pytest)
quality:
	bash scripts/quality.sh

# Ejecutar pruebas con Pytest
test:
	pytest -v --cov=app --cov-report=term-missing

# Levantar servidor local de FastAPI con Uvicorn
run:
	uvicorn app.main:app --reload

# Limpiar archivos temporales
clean:
	rm -rf __pycache__/ .pytest_cache/ .mypy_cache/ htmlcov/ .coverage
