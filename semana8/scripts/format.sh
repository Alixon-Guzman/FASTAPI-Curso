#!/bin/bash
set -e

echo "===> Formateando código con Black..."
black app tests

echo "===> Ordenando imports con isort..."
isort app tests

echo "✅ Formato aplicado correctamente."
