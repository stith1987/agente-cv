#!/bin/bash
# Script para iniciar API y UI en modo desarrollo

# Iniciar API en background
uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload &
API_PID=$!

# Esperar un momento para que la API inicie
sleep 3

# Iniciar Gradio UI
python api/ui_gradio.py &
UI_PID=$!

# Función para limpiar al salir
cleanup() {
    echo "Deteniendo servicios..."
    kill $API_PID $UI_PID 2>/dev/null
    exit 0
}

# Capturar señal de terminación
trap cleanup SIGTERM SIGINT

# Esperar a que terminen los procesos
wait
