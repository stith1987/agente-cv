@echo off
REM Script de Windows para inicializar ramas Git

echo.
echo ================================
echo CONFIGURACION DE RAMAS GIT
echo ================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    echo Por favor instala Python 3.7 o superior
    pause
    exit /b 1
)

REM Ejecutar el script de Python
python scripts\setup_branches.py

echo.
pause
