#!/bin/bash
set -e

echo "===> Ejecutando Flake8..."
flake8 app tests

echo "✅ Linter completado sin errores."
