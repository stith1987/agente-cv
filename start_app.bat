@echo off
echo ============================================
echo    CV Agent - Iniciando Aplicacion
echo ============================================

cd /d "c:\Users\eduar\OneDrive\Documentos\Agentes cursos\agente-cv"

echo Activando entorno virtual...
call .venv\Scripts\activate.bat

echo Configurando variables de entorno...
set PYTHONPATH=.
set API_BASE_URL=http://localhost:8000

echo.
echo ============================================
echo  Ejecutando API en Puerto 8000
echo ============================================
echo.

start "CV Agent API" cmd /k "python api\app.py"

echo Esperando 10 segundos para que la API se inicie...
timeout /t 10 /nobreak

echo.
echo ============================================
echo  Ejecutando UI de Gradio en Puerto 7860
echo ============================================
echo.

start "CV Agent UI" cmd /k "python api\ui_gradio.py"

echo.
echo ============================================
echo          SERVICIOS INICIADOS
echo ============================================
echo  API: http://localhost:8000
echo  UI:  http://localhost:7860
echo  Docs: http://localhost:8000/docs
echo ============================================
echo.
echo Presiona cualquier tecla para cerrar...
pause