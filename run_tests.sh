#!/bin/bash
# Script para ejecutar pruebas automatizadas con Selenium
# Genera reporte HTML con pytest-html

set -e

echo "=========================================="
echo "Pruebas Automatizadas - Patio de Juegos"
echo "=========================================="
echo ""

# Verificar que el servidor está corriendo
echo "Verificando servidor web en http://localhost:8000..."
if ! curl -s http://localhost:8000 > /dev/null 2>&1; then
    echo "⚠️  Servidor no detectado en localhost:8000"
    echo "Inicia el servidor con: cd docs && python3 -m http.server 8000"
    echo ""
    read -p "¿Continuar de todas formas? (s/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
fi

# Navegar al directorio de pruebas
cd "$(dirname "$0")"
cd tests/automation

# Crear directorio de reportes
mkdir -p ../../reports

# Ejecutar pruebas con pytest y generar reporte HTML
echo ""
echo "Ejecutando pruebas..."
echo ""

python3 -m pytest test_cases/ \
    -v \
    --html=../../reports/test_report.html \
    --self-contained-html \
    --tb=short \
    -ra

echo ""
echo "=========================================="
echo "✓ Pruebas completadas"
echo "=========================================="
echo ""
echo "Reporte HTML generado en: reports/test_report.html"
echo "Screenshots guardados en: reports/screenshots/"
echo ""
