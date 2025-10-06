#!/bin/bash
# Script para gestionar Docker en agente-cv (Linux/Mac)
# Uso: ./docker_manager.sh [comando]

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

function print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

function print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

function print_info() {
    echo -e "${YELLOW}[INFO]${NC} $1"
}

function show_menu() {
    echo "========================================"
    echo "   Docker Manager - agente-cv"
    echo "========================================"
    echo ""
    echo "Comandos disponibles:"
    echo ""
    echo "  build    - Construir las imágenes Docker"
    echo "  up       - Iniciar los servicios"
    echo "  down     - Detener los servicios"
    echo "  logs     - Ver logs en tiempo real"
    echo "  restart  - Reiniciar los servicios"
    echo "  clean    - Limpiar contenedores y volúmenes"
    echo "  status   - Ver estado de los servicios"
    echo "  shell    - Abrir shell en el contenedor"
    echo ""
    echo "Uso: ./docker_manager.sh [comando]"
    echo "Ejemplo: ./docker_manager.sh up"
}

function build_images() {
    print_info "Construyendo imágenes Docker..."
    if docker-compose build --no-cache; then
        print_success "Imágenes construidas exitosamente"
    else
        print_error "Falló al construir las imágenes"
        exit 1
    fi
}

function start_services() {
    print_info "Iniciando servicios..."
    if docker-compose up -d; then
        print_success "Servicios iniciados"
        echo ""
        echo "Aplicación disponible en:"
        echo "  - API: http://localhost:8000"
        echo "  - UI:  http://localhost:7860"
        echo "  - Docs: http://localhost:8000/docs"
    else
        print_error "Falló al iniciar servicios"
        exit 1
    fi
}

function stop_services() {
    print_info "Deteniendo servicios..."
    if docker-compose down; then
        print_success "Servicios detenidos"
    else
        print_error "Falló al detener servicios"
        exit 1
    fi
}

function show_logs() {
    print_info "Mostrando logs (Ctrl+C para salir)..."
    docker-compose logs -f
}

function restart_services() {
    print_info "Reiniciando servicios..."
    if docker-compose restart; then
        print_success "Servicios reiniciados"
    else
        print_error "Falló al reiniciar servicios"
        exit 1
    fi
}

function clean_all() {
    print_info "¿Estás seguro? Esto eliminará contenedores y volúmenes (s/n)"
    read -r confirm
    if [[ $confirm == [sS] ]]; then
        print_info "Limpiando..."
        docker-compose down -v
        docker system prune -f
        print_success "Limpieza completada"
    else
        print_info "Operación cancelada"
    fi
}

function show_status() {
    print_info "Estado de los servicios:"
    echo ""
    docker-compose ps
    echo ""
    print_info "Uso de recursos:"
    docker stats --no-stream agente-cv-app 2>/dev/null || echo "Contenedor no está corriendo"
}

function open_shell() {
    print_info "Abriendo shell en el contenedor..."
    docker-compose exec agente-cv bash
}

# Main
case "$1" in
    build)
        build_images
        ;;
    up)
        start_services
        ;;
    down)
        stop_services
        ;;
    logs)
        show_logs
        ;;
    restart)
        restart_services
        ;;
    clean)
        clean_all
        ;;
    status)
        show_status
        ;;
    shell)
        open_shell
        ;;
    *)
        show_menu
        ;;
esac
