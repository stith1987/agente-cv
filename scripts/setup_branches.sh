#!/bin/bash
# Script de Linux/Mac para inicializar ramas Git

set -e

echo ""
echo "================================"
echo "CONFIGURACION DE RAMAS GIT"
echo "================================"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado"
    echo "Por favor instala Python 3.7 o superior"
    exit 1
fi

# Hacer el script ejecutable
chmod +x scripts/setup_branches.py

# Ejecutar el script de Python
python3 scripts/setup_branches.py

echo ""
