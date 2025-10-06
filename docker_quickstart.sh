#!/bin/bash
# Script de Inicio Rápido de Docker para agente-cv
# Este script guía al usuario en el proceso de setup

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo ""
    echo "========================================"
    echo "   $1"
    echo "========================================"
    echo ""
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[AVISO]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker no está instalado"
        echo ""
        echo "Instala Docker desde:"
        echo "https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! docker ps &> /dev/null; then
        print_error "Docker no está corriendo"
        echo ""
        echo "Inicia Docker e intenta de nuevo:"
        echo "  sudo systemctl start docker  # Linux"
        echo "  open -a Docker              # Mac"
        exit 1
    fi
    
    print_success "Docker está instalado y corriendo"
}

check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose no está instalado"
        echo ""
        echo "Instala Docker Compose desde:"
        echo "https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    print_success "Docker Compose está instalado"
}

check_files() {
    local files=("Dockerfile" "docker-compose.yml" "requirements.txt")
    
    for file in "${files[@]}"; do
        if [ ! -f "$file" ]; then
            print_error "Archivo no encontrado: $file"
            exit 1
        fi
    done
    
    print_success "Archivos Docker encontrados"
}

check_env() {
    if [ ! -f ".env" ]; then
        print_warning "Archivo .env no encontrado"
        echo ""
        
        if [ -f ".env.example" ]; then
            print_info "Creando .env desde .env.example..."
            cp .env.example .env
            echo ""
            print_warning "IMPORTANTE: Debes editar .env y agregar tus API keys"
            echo ""
            read -p "¿Abrir .env ahora? (s/n): " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Ss]$ ]]; then
                ${EDITOR:-nano} .env
            fi
        else
            print_error ".env.example tampoco existe"
            exit 1
        fi
    else
        print_success "Archivo .env encontrado"
    fi
}

quick_start() {
    print_header "Inicio Rápido"
    
    print_info "Construyendo imágenes..."
    echo "Esto puede tardar varios minutos la primera vez..."
    echo ""
    
    if docker-compose build; then
        print_success "Construcción exitosa!"
        echo ""
        
        print_info "Iniciando servicios..."
        if docker-compose up -d; then
            echo ""
            print_header "¡Servicios Iniciados!"
            echo ""
            echo "API disponible en:"
            echo "  - http://localhost:8000"
            echo "  - http://localhost:8000/docs"
            echo ""
            echo "UI disponible en:"
            echo "  - http://localhost:7860"
            echo ""
            print_info "Para ver logs en tiempo real:"
            echo "  docker-compose logs -f"
            echo ""
            print_info "Para detener:"
            echo "  docker-compose down"
            echo ""
        else
            print_error "Falló el inicio de servicios"
            exit 1
        fi
    else
        print_error "Falló la construcción"
        exit 1
    fi
}

build_only() {
    print_info "Construyendo imágenes..."
    if docker-compose build --no-cache; then
        print_success "Imágenes construidas exitosamente"
    else
        print_error "Falló la construcción"
        exit 1
    fi
}

start_only() {
    print_info "Iniciando servicios..."
    if docker-compose up -d; then
        print_success "Servicios iniciados"
        echo ""
        echo "API: http://localhost:8000"
        echo "UI:  http://localhost:7860"
    else
        print_error "Falló el inicio"
        exit 1
    fi
}

verify() {
    print_info "Ejecutando verificación..."
    if command -v python3 &> /dev/null; then
        python3 verify_docker.py
    elif command -v python &> /dev/null; then
        python verify_docker.py
    else
        print_error "Python no está instalado"
    fi
}

show_status() {
    print_info "Estado de servicios:"
    echo ""
    docker-compose ps
    echo ""
    print_info "Uso de recursos:"
    docker stats --no-stream agente-cv-app || true
}

show_logs() {
    print_info "Mostrando logs (Ctrl+C para salir)..."
    docker-compose logs -f
}

stop_services() {
    print_info "Deteniendo servicios..."
    docker-compose down
    print_success "Servicios detenidos"
}

clean_all() {
    print_warning "¿Estás seguro? Esto eliminará contenedores y volúmenes (s/n)"
    read -p "> " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        print_info "Limpiando..."
        docker-compose down -v
        docker system prune -f
        print_success "Limpieza completada"
    else
        print_info "Operación cancelada"
    fi
}

show_menu() {
    print_header "Inicio Rápido Docker - agente-cv"
    
    echo "1. Inicio Rápido (Construir + Iniciar)"
    echo "2. Solo Construir imágenes"
    echo "3. Solo Iniciar servicios"
    echo "4. Verificar instalación"
    echo "5. Ver estado de servicios"
    echo "6. Ver logs"
    echo "7. Detener servicios"
    echo "8. Limpiar todo"
    echo "9. Salir"
    echo ""
    read -p "Selecciona una opción (1-9): " choice
    
    case $choice in
        1) quick_start ;;
        2) build_only ;;
        3) start_only ;;
        4) verify ;;
        5) show_status ;;
        6) show_logs ;;
        7) stop_services ;;
        8) clean_all ;;
        9) exit 0 ;;
        *) 
            print_error "Opción inválida"
            show_menu
            ;;
    esac
}

# Main
main() {
    # Verificaciones iniciales
    check_docker
    check_docker_compose
    check_files
    check_env
    
    # Si hay argumentos, ejecutar directamente
    if [ $# -gt 0 ]; then
        case $1 in
            start|up) quick_start ;;
            build) build_only ;;
            run) start_only ;;
            verify|check) verify ;;
            status) show_status ;;
            logs) show_logs ;;
            stop|down) stop_services ;;
            clean) clean_all ;;
            *)
                echo "Uso: $0 [start|build|run|verify|status|logs|stop|clean]"
                exit 1
                ;;
        esac
    else
        # Sin argumentos, mostrar menú
        show_menu
    fi
}

main "$@"
