@echo off
REM Script de Inicio Rápido de Docker para agente-cv
REM Este script guía al usuario en el proceso de setup

echo ========================================
echo   Inicio Rapido Docker - agente-cv
echo ========================================
echo.

REM Verificar si Docker está instalado
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker no esta instalado
    echo.
    echo Descarga Docker Desktop desde:
    echo https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)

REM Verificar si Docker está corriendo
docker ps >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker no esta corriendo
    echo.
    echo Por favor, inicia Docker Desktop e intenta de nuevo
    pause
    exit /b 1
)

echo [OK] Docker esta instalado y corriendo
echo.

REM Verificar archivos necesarios
if not exist "Dockerfile" (
    echo [ERROR] Dockerfile no encontrado
    pause
    exit /b 1
)

if not exist "docker-compose.yml" (
    echo [ERROR] docker-compose.yml no encontrado
    pause
    exit /b 1
)

echo [OK] Archivos Docker encontrados
echo.

REM Verificar archivo .env
if not exist ".env" (
    echo [AVISO] Archivo .env no encontrado
    echo.
    if exist ".env.example" (
        echo Creando .env desde .env.example...
        copy .env.example .env >nul
        echo.
        echo [IMPORTANTE] Debes editar .env y agregar tus API keys
        echo.
        echo Presiona una tecla para abrir .env en el editor...
        pause >nul
        notepad .env
    ) else (
        echo [ERROR] .env.example tampoco existe
        pause
        exit /b 1
    )
)

echo ========================================
echo   Opciones de Inicio
echo ========================================
echo.
echo 1. Inicio Rapido (Construir + Iniciar)
echo 2. Solo Construir imagenes
echo 3. Solo Iniciar servicios
echo 4. Verificar instalacion
echo 5. Ver estado de servicios
echo 6. Ver logs
echo 7. Detener servicios
echo 8. Limpiar todo
echo 9. Salir
echo.
set /p choice="Selecciona una opcion (1-9): "

if "%choice%"=="1" goto quick_start
if "%choice%"=="2" goto build_only
if "%choice%"=="3" goto start_only
if "%choice%"=="4" goto verify
if "%choice%"=="5" goto status
if "%choice%"=="6" goto logs
if "%choice%"=="7" goto stop
if "%choice%"=="8" goto clean
if "%choice%"=="9" goto end
goto menu

:quick_start
echo.
echo [INICIO RAPIDO] Construyendo e iniciando servicios...
echo.
echo Esto puede tardar varios minutos la primera vez...
echo.
docker-compose build
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo la construccion
    pause
    goto end
)
echo.
echo [BUILD] Construccion exitosa!
echo.
docker-compose up -d
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo el inicio
    pause
    goto end
)
echo.
echo ========================================
echo   Servicios Iniciados!
echo ========================================
echo.
echo API disponible en:
echo   - http://localhost:8000
echo   - http://localhost:8000/docs
echo.
echo UI disponible en:
echo   - http://localhost:7860
echo.
echo Para ver logs en tiempo real:
echo   docker-compose logs -f
echo.
echo Para detener:
echo   docker-compose down
echo.
pause
goto end

:build_only
echo.
echo [BUILD] Construyendo imagenes...
docker-compose build --no-cache
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo la construccion
) else (
    echo [OK] Imagenes construidas exitosamente
)
pause
goto end

:start_only
echo.
echo [START] Iniciando servicios...
docker-compose up -d
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo el inicio
) else (
    echo [OK] Servicios iniciados
    echo.
    echo API: http://localhost:8000
    echo UI:  http://localhost:7860
)
pause
goto end

:verify
echo.
echo [VERIFY] Ejecutando verificacion...
python verify_docker.py
pause
goto end

:status
echo.
echo [STATUS] Estado de servicios:
echo.
docker-compose ps
echo.
echo Uso de recursos:
docker stats --no-stream agente-cv-app
pause
goto end

:logs
echo.
echo [LOGS] Mostrando logs (Ctrl+C para salir)...
docker-compose logs -f
goto end

:stop
echo.
echo [STOP] Deteniendo servicios...
docker-compose down
echo [OK] Servicios detenidos
pause
goto end

:clean
echo.
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
pause
goto end

:end
echo.
echo Gracias por usar agente-cv!
echo.
