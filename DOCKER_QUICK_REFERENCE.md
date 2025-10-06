# 🚀 Guía de Referencia Rápida - Docker agente-cv

## Comandos Esenciales

### 🏁 Inicio

```bash
docker-compose up -d                    # Iniciar en background
docker-compose up                       # Iniciar con logs en consola
docker_quickstart.bat                   # Windows: Script interactivo
./docker_quickstart.sh                  # Linux/Mac: Script interactivo
make up                                 # Con Makefile
```

### 🛑 Detener

```bash
docker-compose down                     # Detener servicios
docker-compose down -v                  # Detener + eliminar volúmenes
docker-compose stop                     # Pausar servicios
```

### 🔄 Reiniciar

```bash
docker-compose restart                  # Reiniciar todos
docker-compose restart agente-cv        # Reiniciar uno específico
```

### 📊 Estado y Monitoreo

```bash
docker-compose ps                       # Ver servicios
docker-compose logs -f                  # Ver logs en tiempo real
docker-compose logs --tail=100          # Últimas 100 líneas
docker stats                            # Uso de recursos
docker-compose top                      # Procesos corriendo
```

### 🔨 Build

```bash
docker-compose build                    # Construir imágenes
docker-compose build --no-cache         # Sin caché
docker-compose up -d --build            # Rebuild + start
```

### 🐚 Shell y Debugging

```bash
docker-compose exec agente-cv bash      # Shell interactiva
docker-compose exec agente-cv python    # Python REPL
docker-compose exec -u root agente-cv bash  # Como root
```

### 🧹 Limpieza

```bash
docker-compose down -v                  # Eliminar todo
docker system prune -f                  # Limpiar sistema
docker volume prune -f                  # Limpiar volúmenes
docker image prune -a -f                # Limpiar imágenes
```

---

## Casos de Uso Comunes

### 📝 Ver logs de errores

```bash
docker-compose logs | grep ERROR
docker-compose logs | grep -i "error\|exception\|failed"
docker-compose logs --tail=200 agente-cv | grep ERROR
```

### 🔍 Inspeccionar contenedor

```bash
docker inspect agente-cv-app                        # Info completa
docker inspect agente-cv-app | grep -A 5 State     # Estado
docker inspect agente-cv-app | grep -A 10 Health   # Health check
```

### 📦 Gestión de volúmenes

```bash
docker volume ls                                    # Listar volúmenes
docker volume inspect agente-cv_agente-data        # Ver detalles
docker run --rm -v agente-cv_agente-data:/data alpine ls -la /data  # Ver contenido
```

### 🌐 Networking

```bash
docker network ls                                   # Listar redes
docker network inspect agente-cv_agente-network    # Ver detalles de red
docker-compose exec agente-cv ping google.com      # Test conectividad
```

### 🔐 Variables de entorno

```bash
docker-compose exec agente-cv env                  # Ver todas las vars
docker-compose exec agente-cv env | grep API_KEY  # Filtrar por nombre
docker-compose config                              # Ver config completa
```

### 📊 Performance

```bash
docker stats --no-stream                           # Snapshot de recursos
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
docker-compose exec agente-cv top                  # Procesos dentro
```

---

## Scripts Personalizados

### Windows

```cmd
docker_manager.bat build        # Construir
docker_manager.bat up           # Iniciar
docker_manager.bat logs         # Ver logs
docker_manager.bat status       # Estado
docker_manager.bat shell        # Shell
docker_manager.bat clean        # Limpiar
```

### Linux/Mac

```bash
./docker_manager.sh build       # Construir
./docker_manager.sh up          # Iniciar
./docker_manager.sh logs        # Ver logs
./docker_manager.sh status      # Estado
./docker_manager.sh shell       # Shell
./docker_manager.sh clean       # Limpiar
```

### Make

```bash
make build          # Construir
make up             # Iniciar
make down           # Detener
make logs           # Ver logs
make status         # Estado
make shell          # Shell
make clean          # Limpiar
make dev            # Modo desarrollo
make prod           # Modo producción
make test           # Ejecutar tests
```

---

## Configuraciones por Entorno

### Desarrollo

```bash
# Con hot-reload y debug
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# O con make
make dev
```

### Producción

```bash
# Optimizado con límites de recursos
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# O con make
make prod
```

### Escalado

```bash
# Múltiples réplicas con load balancer
docker-compose -f docker-compose.scaled.yml up -d --scale agente-cv=3

# Verificar réplicas
docker-compose -f docker-compose.scaled.yml ps
```

---

## Testing y Verificación

### Health Checks

```bash
# Verificar health
curl http://localhost:8000/health
docker inspect agente-cv-app | grep -A 10 Health

# Script de verificación
python healthcheck.py
```

### API Testing

```bash
# Test endpoint
curl http://localhost:8000/docs

# Test chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'

# Ver OpenAPI spec
curl http://localhost:8000/openapi.json
```

### Verificación Pre-Deploy

```bash
# Script de verificación completo
python verify_docker.py

# Validar docker-compose.yml
docker-compose config

# Verificar puertos
netstat -an | grep -E "8000|7860"  # Linux/Mac
netstat -an | findstr "8000 7860"  # Windows
```

---

## Backups y Restauración

### Backup

```bash
# Backup de volúmenes
docker run --rm \
  -v agente-cv_agente-data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/data-$(date +%Y%m%d).tar.gz /data

# O con make
make backup
```

### Restore

```bash
# Restaurar desde backup
docker run --rm \
  -v agente-cv_agente-data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar xzf /backup/data-20240101.tar.gz -C /
```

---

## Troubleshooting Rápido

### Contenedor no inicia

```bash
docker-compose logs --tail=100 agente-cv
docker inspect agente-cv-app | grep ExitCode
docker-compose up  # Sin -d para ver errores
```

### Puerto ocupado

```bash
# Windows
Get-NetTCPConnection -LocalPort 8000
# Linux/Mac
lsof -i :8000

# Cambiar puerto
# Edita docker-compose.yml: "8001:8000"
```

### Alto uso de recursos

```bash
docker stats
docker-compose restart agente-cv
docker system prune -f
```

### Permisos

```bash
# Linux/Mac
sudo chown -R $USER:$USER logs/ storage/
chmod -R 755 logs/ storage/

# Windows: ejecutar PowerShell como Admin
```

---

## URLs de Acceso

```
API REST:       http://localhost:8000
API Docs:       http://localhost:8000/docs
API Redoc:      http://localhost:8000/redoc
OpenAPI:        http://localhost:8000/openapi.json
Health:         http://localhost:8000/health
Gradio UI:      http://localhost:7860
```

---

## Variables de Entorno Importantes

```bash
# En .env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GROQ_API_KEY=gsk_...
GOOGLE_API_KEY=...
MISTRAL_API_KEY=...

HOST=0.0.0.0
PORT=8000
DEBUG=false
LOG_LEVEL=INFO
```

---

## Más Información

- 📖 **Guía Completa**: [README_DOCKER.md](README_DOCKER.md)
- 🏆 **Mejores Prácticas**: [DOCKER_BEST_PRACTICES.md](DOCKER_BEST_PRACTICES.md)
- 🔧 **Troubleshooting**: [DOCKER_TROUBLESHOOTING.md](DOCKER_TROUBLESHOOTING.md)
- 📦 **Resumen**: [DOCKER_SUMMARY.md](DOCKER_SUMMARY.md)

---

**💡 Tip**: Guarda esta página en tus favoritos para acceso rápido a los comandos más usados.
