@echo off
REM Script para gestionar Docker en agente-cv
REM Uso: docker_manager.bat [comando]

echo ========================================
echo   Docker Manager - agente-cv
echo ========================================
echo.

if "%1"=="" goto menu
if "%1"=="build" goto build
if "%1"=="up" goto up
if "%1"=="down" goto down
if "%1"=="logs" goto logs
if "%1"=="restart" goto restart
if "%1"=="clean" goto clean
if "%1"=="status" goto status
if "%1"=="shell" goto shell
goto menu

:menu
echo Comandos disponibles:
echo.
echo   build    - Construir las imagenes Docker
echo   up       - Iniciar los servicios
echo   down     - Detener los servicios
echo   logs     - Ver logs en tiempo real
echo   restart  - Reiniciar los servicios
echo   clean    - Limpiar contenedores y volumenes
echo   status   - Ver estado de los servicios
echo   shell    - Abrir shell en el contenedor
echo.
echo Uso: docker_manager.bat [comando]
echo Ejemplo: docker_manager.bat up
echo.
goto end

:build
echo [BUILD] Construyendo imagenes Docker...
docker-compose build --no-cache
if %ERRORLEVEL% EQU 0 (
    echo [OK] Imagenes construidas exitosamente
) else (
    echo [ERROR] Fallo al construir las imagenes
)
goto end

:up
echo [UP] Iniciando servicios...
docker-compose up -d
if %ERRORLEVEL% EQU 0 (
    echo [OK] Servicios iniciados
    echo.
    echo Aplicacion disponible en:
    echo   - API: http://localhost:8000
    echo   - UI:  http://localhost:7860
    echo   - Docs: http://localhost:8000/docs
) else (
    echo [ERROR] Fallo al iniciar servicios
)
goto end

:down
echo [DOWN] Deteniendo servicios...
docker-compose down
if %ERRORLEVEL% EQU 0 (
    echo [OK] Servicios detenidos
) else (
    echo [ERROR] Fallo al detener servicios
)
goto end

:logs
echo [LOGS] Mostrando logs (Ctrl+C para salir)...
docker-compose logs -f
goto end

:restart
echo [RESTART] Reiniciando servicios...
docker-compose restart
if %ERRORLEVEL% EQU 0 (
    echo [OK] Servicios reiniciados
) else (
    echo [ERROR] Fallo al reiniciar servicios
)
goto end

:clean
echo [CLEAN] ¿Estas seguro? Esto eliminara contenedores y volumenes (S/N)
set /p confirm=
if /i "%confirm%"=="S" (
    echo Limpiando...
    docker-compose down -v
    docker system prune -f
    echo [OK] Limpieza completada
) else (
    echo [CANCELADO] Operacion cancelada
)
goto end

:status
echo [STATUS] Estado de los servicios:
echo.
docker-compose ps
echo.
echo Uso de recursos:
docker stats --no-stream agente-cv-app
goto end

:shell
echo [SHELL] Abriendo shell en el contenedor...
docker-compose exec agente-cv bash
goto end

:end
echo.
pause
