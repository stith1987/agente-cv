.PHONY: help build up down logs restart clean status shell test dev prod

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles para agente-cv:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Construir las imágenes Docker
	@echo "🔨 Construyendo imágenes..."
	docker-compose build --no-cache

up: ## Iniciar todos los servicios
	@echo "🚀 Iniciando servicios..."
	docker-compose up -d
	@echo "✅ Servicios iniciados!"
	@echo "📍 API: http://localhost:8000"
	@echo "📍 UI:  http://localhost:7860"
	@echo "📍 Docs: http://localhost:8000/docs"

down: ## Detener todos los servicios
	@echo "🛑 Deteniendo servicios..."
	docker-compose down

logs: ## Ver logs en tiempo real
	docker-compose logs -f

restart: ## Reiniciar servicios
	@echo "🔄 Reiniciando servicios..."
	docker-compose restart

clean: ## Limpiar contenedores y volúmenes
	@echo "🧹 Limpiando..."
	docker-compose down -v
	docker system prune -f
	@echo "✅ Limpieza completada"

status: ## Ver estado de los servicios
	@echo "📊 Estado de los servicios:"
	docker-compose ps
	@echo ""
	@echo "💻 Uso de recursos:"
	docker stats --no-stream agente-cv-app || true

shell: ## Abrir shell en el contenedor
	docker-compose exec agente-cv bash

test: ## Ejecutar tests en el contenedor
	docker-compose exec agente-cv python -m pytest

dev: ## Iniciar en modo desarrollo
	@echo "🔧 Iniciando en modo desarrollo..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

prod: ## Iniciar en modo producción
	@echo "🏭 Iniciando en modo producción..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

rebuild: ## Reconstruir y reiniciar
	@echo "🔨 Reconstruyendo..."
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d
	@echo "✅ Reconstrucción completada"

backup: ## Backup de datos
	@echo "💾 Creando backup..."
	@mkdir -p backups
	tar -czf backups/backup-$(shell date +%Y%m%d-%H%M%S).tar.gz data/ storage/ logs/
	@echo "✅ Backup creado en backups/"

install-hooks: ## Instalar pre-commit hooks
	@echo "🪝 Instalando hooks..."
	chmod +x docker_manager.sh
	@echo "✅ Hooks instalados"
