#!/bin/bash
set -e

echo "===> Verificando formato (Black)..."
black --check app tests

echo "===> Verificando imports (isort)..."
isort --check-only app tests

echo "===> Ejecutando Flake8..."
flake8 app tests

echo "===> Ejecutando MyPy..."
mypy app

echo "===> Ejecutando Bandit..."
bandit -r app

echo "===> Ejecutando pruebas con Pytest..."
pytest --cov=app --cov-report=term-missing --cov-fail-under=80

echo "✅ Todas las verificaciones pasaron correctamente."
