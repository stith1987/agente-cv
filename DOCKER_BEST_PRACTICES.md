# 🐳 Mejores Prácticas Docker - agente-cv

## 📋 Checklist Pre-Despliegue

### Seguridad

- [ ] Variables de entorno en `.env` (nunca en el código)
- [ ] API keys configuradas correctamente
- [ ] Puerto 8000 y 7860 no expuestos públicamente sin autenticación
- [ ] Imagen base actualizada (`python:3.11-slim`)
- [ ] Sin credenciales hardcodeadas
- [ ] `.env` en `.gitignore`

### Optimización

- [ ] `.dockerignore` configurado correctamente
- [ ] Multi-stage build (si aplica)
- [ ] Caché de Docker Buildx habilitado
- [ ] Volúmenes para datos persistentes
- [ ] Health checks configurados
- [ ] Límites de recursos definidos

### Monitoreo

- [ ] Logs configurados y rotativos
- [ ] Health endpoint funcionando
- [ ] Métricas expuestas
- [ ] Alertas configuradas

## 🏗️ Arquitectura de Contenedores

```
┌─────────────────────────────────────────┐
│         agente-cv Container             │
│                                         │
│  ┌──────────┐      ┌──────────┐       │
│  │ FastAPI  │◄────►│  Gradio  │       │
│  │  :8000   │      │  :7860   │       │
│  └──────────┘      └──────────┘       │
│       │                  │             │
│       ▼                  ▼             │
│  ┌──────────────────────────┐         │
│  │    Orchestrator          │         │
│  │    (Agent Core)          │         │
│  └──────────────────────────┘         │
│       │         │         │            │
│       ▼         ▼         ▼            │
│  ┌──────┐  ┌──────┐  ┌──────┐        │
│  │ RAG  │  │ FAQ  │  │Email │        │
│  │      │  │ SQL  │  │Agent │        │
│  └──────┘  └──────┘  └──────┘        │
└─────────────────────────────────────────┘
         │         │         │
         ▼         ▼         ▼
    ┌────────┐ ┌────────┐ ┌────────┐
    │Volumes │ │Volumes │ │Volumes │
    │ data/  │ │ logs/  │ │storage/│
    └────────┘ └────────┘ └────────┘
```

## 🚀 Estrategias de Despliegue

### Desarrollo Local

```bash
# Usar el compose de desarrollo con hot-reload
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Ventajas:
# - Cambios en tiempo real
# - Debug habilitado
# - Logs detallados
```

### Staging/QA

```bash
# Similar a producción pero con más logs
docker-compose -f docker-compose.yml up

# Recomendaciones:
# - Usar datos de prueba
# - Habilitar métricas detalladas
# - Testing automatizado
```

### Producción

```bash
# Usar configuración optimizada
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Consideraciones:
# - Límites de recursos
# - Logs rotativos
# - Health checks estrictos
# - Reinicio automático
# - Backups programados
```

## 🔐 Gestión de Secretos

### Opción 1: Variables de Entorno (Desarrollo)

```bash
# .env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

### Opción 2: Docker Secrets (Producción)

```yaml
# docker-compose.prod.yml
services:
  agente-cv:
    secrets:
      - openai_key
      - anthropic_key
    environment:
      - OPENAI_API_KEY_FILE=/run/secrets/openai_key

secrets:
  openai_key:
    file: ./secrets/openai.txt
  anthropic_key:
    file: ./secrets/anthropic.txt
```

### Opción 3: Vault/Secret Manager

```bash
# Para AWS Secrets Manager, Azure Key Vault, etc.
# Usar un init container o script de entrada
```

## 📊 Monitoreo y Logs

### Ver Logs en Tiempo Real

```bash
# Todos los servicios
docker-compose logs -f

# Solo errores
docker-compose logs --tail=100 | grep ERROR

# Exportar logs
docker-compose logs --no-color > logs_$(date +%Y%m%d).txt
```

### Configurar Log Rotation

```yaml
# docker-compose.yml
services:
  agente-cv:
    logging:
      driver: 'json-file'
      options:
        max-size: '10m'
        max-file: '3'
```

### Integrar con Sistemas Externos

```yaml
# Ejemplo con ELK Stack
services:
  agente-cv:
    logging:
      driver: 'fluentd'
      options:
        fluentd-address: localhost:24224
        tag: agente-cv
```

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/docker-ci.yml
name: Docker Build & Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build
        run: docker-compose build
      - name: Test
        run: docker-compose run agente-cv pytest
      - name: Deploy
        run: |
          # Comandos de despliegue
```

## 🐛 Debugging

### Entrar al Contenedor

```bash
# Shell interactivo
docker-compose exec agente-cv bash

# Ver procesos
docker-compose exec agente-cv ps aux

# Verificar conectividad
docker-compose exec agente-cv ping google.com
```

### Verificar Configuración

```bash
# Variables de entorno
docker-compose exec agente-cv env

# Archivos montados
docker-compose exec agente-cv ls -la /app

# Permisos
docker-compose exec agente-cv ls -l /app/logs
```

### Probar Endpoints

```bash
# Health check
curl http://localhost:8000/health

# API docs
curl http://localhost:8000/docs

# Chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "¿Cuál es tu experiencia?"}'
```

## 🔧 Optimizaciones de Performance

### Multi-stage Build

```dockerfile
# Ejemplo de multi-stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*
COPY . .
CMD ["python", "run_full_app.py"]
```

### Caché de Dependencias

```bash
# Usar BuildKit para mejor caché
DOCKER_BUILDKIT=1 docker-compose build

# O en docker-compose.yml
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1
```

### Reducir Tamaño de Imagen

```dockerfile
# Usar alpine si es compatible
FROM python:3.11-alpine

# Limpiar cache después de instalar
RUN pip install --no-cache-dir -r requirements.txt

# Eliminar archivos temporales
RUN rm -rf /tmp/* /var/tmp/*
```

## 📦 Gestión de Volúmenes

### Backup

```bash
# Backup manual
docker run --rm \
  -v agente-cv_agente-data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/data-$(date +%Y%m%d).tar.gz /data

# Script automático en cron
0 2 * * * /path/to/backup-script.sh
```

### Restore

```bash
# Restaurar desde backup
docker run --rm \
  -v agente-cv_agente-data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar xzf /backup/data-20240101.tar.gz -C /
```

## 🔍 Health Checks Avanzados

### Health Check Personalizado

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python healthcheck.py || exit 1
```

### Monitoreo Externo

```bash
# Usar herramientas como:
# - Prometheus + Grafana
# - DataDog
# - New Relic
# - Uptime Robot
```

## 🌐 Networking

### Red Personalizada

```yaml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true # Sin acceso a internet
```

### Límites de Red

```yaml
services:
  agente-cv:
    networks:
      frontend:
        ipv4_address: 172.20.0.5
    sysctls:
      - net.ipv4.tcp_syncookies=1
```

## 🛡️ Seguridad Hardening

### Usuario No-Root

```dockerfile
# Crear usuario sin privilegios
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser
```

### Read-Only Filesystem

```yaml
services:
  agente-cv:
    read_only: true
    tmpfs:
      - /tmp
      - /app/logs
```

### Security Scanning

```bash
# Trivy
trivy image agente-cv:latest

# Snyk
snyk container test agente-cv:latest

# Clair
clairctl analyze agente-cv:latest
```

## 📈 Escalabilidad

### Múltiples Réplicas

```bash
# Escalar servicios
docker-compose up -d --scale agente-cv=3

# Load balancer con nginx
# Ver nginx.conf ejemplo
```

### Orquestación con Kubernetes

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agente-cv
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agente-cv
  template:
    metadata:
      labels:
        app: agente-cv
    spec:
      containers:
        - name: agente-cv
          image: agente-cv:latest
          ports:
            - containerPort: 8000
```

## 📝 Checklist de Mantenimiento

### Diario

- [ ] Revisar logs de errores
- [ ] Verificar health checks
- [ ] Monitorear uso de recursos

### Semanal

- [ ] Actualizar dependencias de seguridad
- [ ] Revisar métricas de performance
- [ ] Backup de datos

### Mensual

- [ ] Actualizar imagen base
- [ ] Revisar y optimizar Dockerfile
- [ ] Pruebas de disaster recovery
- [ ] Auditoría de seguridad

## 🆘 Troubleshooting Común

### Problema: Contenedor se reinicia constantemente

```bash
# Ver por qué falla
docker-compose logs --tail=100 agente-cv

# Verificar exit code
docker inspect agente-cv-app --format='{{.State.ExitCode}}'

# Posibles causas:
# - Error en el comando de inicio
# - Faltan variables de entorno
# - Puerto ya en uso
# - Health check fallando
```

### Problema: Alto uso de memoria

```bash
# Ver uso actual
docker stats agente-cv-app

# Limitar memoria
docker-compose up -d --scale agente-cv=1 --memory="2g"

# Investigar memory leaks
docker-compose exec agente-cv python -m memory_profiler app.py
```

### Problema: Lentitud en la aplicación

```bash
# Profiling
docker-compose exec agente-cv python -m cProfile -o output.stats run_full_app.py

# Ver IO stats
docker stats --format "table {{.Container}}\t{{.BlockIO}}"

# Optimizar:
# - Añadir índices a DB
# - Implementar caché
# - Optimizar queries
```

---

**Última actualización**: Octubre 2025
**Mantenedor**: Eduardo (stith1987)
