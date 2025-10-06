# 🐳 Guía de Docker para agente-cv

Esta guía te ayudará a ejecutar la aplicación agente-cv usando Docker y Docker Compose.

## 📋 Requisitos Previos

- Docker instalado (versión 20.10 o superior)
- Docker Compose instalado (versión 2.0 o superior)
- Al menos 2GB de RAM disponible
- Espacio en disco: ~5GB

## 🚀 Inicio Rápido

### 1. Configurar Variables de Entorno

Copia el archivo de ejemplo y configura tus API keys:

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus claves API:

```bash
notepad .env  # En Windows
# o
nano .env     # En Linux/Mac
```

### 2. Construir y Ejecutar

#### Opción A: Aplicación Completa (API + UI)

```bash
docker-compose up -d
```

Esto iniciará:

- FastAPI en: http://localhost:8000
- Gradio UI en: http://localhost:7860
- API Docs en: http://localhost:8000/docs

#### Opción B: Solo API

```bash
docker-compose --profile api-only up -d
```

API disponible en: http://localhost:8001

#### Opción C: API y UI por separado

```bash
docker-compose --profile api-only --profile ui-only up -d
```

- API en: http://localhost:8001
- UI en: http://localhost:7861

## 🛠️ Comandos Útiles

### Ver logs en tiempo real

```bash
# Todos los servicios
docker-compose logs -f

# Solo la app principal
docker-compose logs -f agente-cv

# Últimas 100 líneas
docker-compose logs --tail=100 -f agente-cv
```

### Detener los servicios

```bash
docker-compose down
```

### Detener y eliminar volúmenes (¡Cuidado! Borra datos persistentes)

```bash
docker-compose down -v
```

### Reconstruir las imágenes

```bash
docker-compose build --no-cache
docker-compose up -d
```

### Ver estado de los contenedores

```bash
docker-compose ps
```

### Ejecutar comandos dentro del contenedor

```bash
# Abrir una shell interactiva
docker-compose exec agente-cv bash

# Ejecutar un comando específico
docker-compose exec agente-cv python test_agentic.py
```

### Reiniciar un servicio específico

```bash
docker-compose restart agente-cv
```

## 📦 Estructura de Volúmenes

Los siguientes directorios se persisten fuera del contenedor:

- `./data` → Datos de CV y proyectos
- `./logs` → Archivos de log
- `./storage` → Base de datos y vectores
- `./config` → Archivos de configuración

## 🔧 Configuración Avanzada

### Cambiar Puertos

Edita `docker-compose.yml`:

```yaml
ports:
  - '8080:8000' # Cambia 8080 al puerto que prefieras
  - '7870:7860' # Cambia 7870 al puerto que prefieras
```

### Añadir Más Memoria

```yaml
services:
  agente-cv:
    # ... otras configuraciones
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 2G
```

### Variables de Entorno Adicionales

Añade al archivo `.env` o directamente en `docker-compose.yml`:

```yaml
environment:
  - TU_VARIABLE=valor
```

## 🐛 Troubleshooting

### Problema: El contenedor no inicia

```bash
# Ver logs detallados
docker-compose logs agente-cv

# Verificar el healthcheck
docker inspect agente-cv-app | grep -A 10 Health
```

### Problema: Puerto ya en uso

```bash
# En Windows PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess

# Cambiar el puerto en docker-compose.yml
ports:
  - "8001:8000"
```

### Problema: Cambios en el código no se reflejan

```bash
# Reconstruir sin caché
docker-compose build --no-cache
docker-compose up -d
```

### Problema: Permisos en volúmenes (Linux/Mac)

```bash
# Dar permisos al directorio
sudo chown -R $USER:$USER ./logs ./storage
```

## 🔒 Seguridad

### Mejores Prácticas

1. **Nunca** subas el archivo `.env` al repositorio
2. Usa secrets de Docker para producción
3. Limita recursos en `docker-compose.yml`
4. Mantén las imágenes actualizadas:

```bash
docker-compose pull
docker-compose up -d
```

## 📊 Monitoreo

### Ver uso de recursos

```bash
docker stats agente-cv-app
```

### Healthcheck

```bash
# Verificar estado de salud
docker inspect agente-cv-app | grep -A 10 Health

# O visitar directamente
curl http://localhost:8000/health
```

## 🚢 Despliegue en Producción

### Usando Docker Compose

```bash
# Usar archivo de producción
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Push a Docker Registry

```bash
# Tag de la imagen
docker tag agente-cv:latest tu-usuario/agente-cv:latest

# Push al registry
docker push tu-usuario/agente-cv:latest
```

## 📝 Notas Adicionales

- El contenedor usa Python 3.11 slim para optimizar tamaño
- Los logs se rotan automáticamente
- El healthcheck verifica el endpoint `/health` cada 30s
- La aplicación se reinicia automáticamente si falla

## 🆘 Soporte

Si encuentras problemas:

1. Revisa los logs: `docker-compose logs -f`
2. Verifica el estado: `docker-compose ps`
3. Revisa el healthcheck del contenedor
4. Consulta la documentación principal del proyecto

## 🔄 Actualizar la Aplicación

```bash
# Detener servicios
docker-compose down

# Actualizar código (git pull, etc.)
git pull origin main

# Reconstruir y reiniciar
docker-compose build
docker-compose up -d
```

---

**¡Listo!** Tu aplicación agente-cv debería estar corriendo en Docker. 🎉
