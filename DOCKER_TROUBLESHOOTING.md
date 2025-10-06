# 🔧 Guía de Troubleshooting Docker - agente-cv

## 📋 Tabla de Contenidos

1. [Problemas Comunes](#problemas-comunes)
2. [Errores de Build](#errores-de-build)
3. [Errores de Ejecución](#errores-de-ejecución)
4. [Problemas de Red](#problemas-de-red)
5. [Problemas de Volúmenes](#problemas-de-volúmenes)
6. [Performance Issues](#performance-issues)
7. [Comandos de Diagnóstico](#comandos-de-diagnóstico)

---

## 🐛 Problemas Comunes

### 1. Contenedor no inicia o se reinicia constantemente

**Síntomas:**

```bash
$ docker-compose ps
NAME                COMMAND             SERVICE    STATUS
agente-cv-app       "python run_..."    agente-cv  Restarting
```

**Diagnóstico:**

```bash
# Ver los últimos logs
docker-compose logs --tail=50 agente-cv

# Ver el exit code
docker inspect agente-cv-app | grep -A 5 "State"

# Ver el comando que ejecutó
docker inspect agente-cv-app | grep -A 2 "Cmd"
```

**Soluciones:**

#### A. Error en variables de entorno

```bash
# Verificar que existe .env
ls -la .env

# Verificar contenido
cat .env | grep -v "^#" | grep -v "^$"

# Crear desde ejemplo
cp .env.example .env
# Editar y agregar tus API keys
```

#### B. Puerto ya en uso

```powershell
# En Windows PowerShell
Get-NetTCPConnection -LocalPort 8000 | Select-Object LocalPort, OwningProcess
Get-Process -Id <PID>

# Matar el proceso
Stop-Process -Id <PID> -Force
```

```bash
# En Linux/Mac
lsof -i :8000
kill -9 <PID>
```

#### C. Falta una dependencia

```bash
# Reconstruir sin caché
docker-compose build --no-cache

# Ver qué falta
docker-compose run --rm agente-cv pip list
docker-compose run --rm agente-cv python -c "import [modulo]"
```

---

### 2. "Permission Denied" en volúmenes

**Síntomas:**

```
PermissionError: [Errno 13] Permission denied: '/app/logs/agent.log'
```

**Soluciones:**

```bash
# Linux/Mac: Dar permisos
sudo chown -R $USER:$USER logs/ storage/ data/

# O en docker-compose.yml añadir:
user: "${UID}:${GID}"

# Verificar permisos dentro del contenedor
docker-compose exec agente-cv ls -la /app/logs
```

---

### 3. Cambios en el código no se reflejan

**Problema:** Hiciste cambios pero el contenedor sigue igual.

**Soluciones:**

```bash
# 1. Reconstruir la imagen
docker-compose build

# 2. Recrear el contenedor
docker-compose up -d --force-recreate

# 3. Limpiar caché de build
docker builder prune -f
docker-compose build --no-cache

# 4. Para desarrollo, usa volúmenes de código:
# Edita docker-compose.yml
volumes:
  - ./agent:/app/agent
  - ./api:/app/api
```

---

### 4. Error de conexión a la API

**Síntomas:**

```
curl http://localhost:8000/health
curl: (7) Failed to connect to localhost port 8000
```

**Diagnóstico:**

```bash
# Verificar que el contenedor está corriendo
docker-compose ps

# Verificar puertos
docker-compose port agente-cv 8000

# Ver si el servicio está escuchando
docker-compose exec agente-cv netstat -tuln | grep 8000
```

**Soluciones:**

```bash
# A. Verificar el healthcheck
docker inspect agente-cv-app | grep -A 10 Health

# B. Probar desde dentro del contenedor
docker-compose exec agente-cv curl http://localhost:8000/health

# C. Verificar firewall
# Windows
netsh advfirewall firewall show rule name=all | findstr 8000

# Linux
sudo ufw status
sudo iptables -L -n | grep 8000
```

---

## 🏗️ Errores de Build

### Error 1: "pip install failed"

```
ERROR: Could not find a version that satisfies the requirement...
```

**Solución:**

```dockerfile
# Actualizar pip antes de instalar
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# O especificar versiones en requirements.txt
openai==1.3.0
anthropic==0.5.0
```

### Error 2: "No space left on device"

```bash
# Limpiar imágenes no usadas
docker system prune -a -f

# Ver uso de disco
docker system df

# Limpiar todo (¡CUIDADO!)
docker system prune -a --volumes -f
```

### Error 3: "Context deadline exceeded"

**Problema:** Build muy lento o timeout.

```bash
# Aumentar timeout en daemon.json (Windows/Mac)
# Ubicación:
# - Windows: C:\ProgramData\Docker\config\daemon.json
# - Mac: ~/.docker/daemon.json
# - Linux: /etc/docker/daemon.json

{
  "max-concurrent-downloads": 3,
  "max-concurrent-uploads": 5,
  "max-download-attempts": 5
}

# Reiniciar Docker
# Windows: Restart-Service docker
# Linux: sudo systemctl restart docker
```

---

## 🚀 Errores de Ejecución

### Error 1: "ModuleNotFoundError"

```python
ModuleNotFoundError: No module named 'openai'
```

**Soluciones:**

```bash
# Verificar requirements.txt
cat requirements.txt | grep openai

# Reconstruir
docker-compose build --no-cache

# Instalar manualmente (temporal)
docker-compose exec agente-cv pip install openai
```

### Error 2: "API Key not found"

```
openai.error.AuthenticationError: No API key provided
```

**Solución:**

```bash
# Verificar .env
cat .env | grep OPENAI_API_KEY

# Verificar en el contenedor
docker-compose exec agente-cv env | grep OPENAI

# Reiniciar con nuevas variables
docker-compose down
docker-compose up -d
```

### Error 3: Database/Storage errors

```
sqlite3.OperationalError: unable to open database file
```

**Solución:**

```bash
# Verificar volúmenes
docker volume ls | grep agente

# Crear directorios
mkdir -p storage/sqlite storage/vectordb logs

# Permisos
chmod -R 755 storage/ logs/

# Recrear volúmenes
docker-compose down -v
docker-compose up -d
```

---

## 🌐 Problemas de Red

### Contenedores no se comunican entre sí

```bash
# Verificar red
docker network ls
docker network inspect agente-cv_agente-network

# Probar conectividad
docker-compose exec agente-cv ping agente-cv-api

# Verificar DNS
docker-compose exec agente-cv nslookup agente-cv-api
```

### Puerto ya en uso

```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "8001:8000"  # host:container

# O detener el proceso que usa el puerto
# Ver sección "Puerto ya en uso" arriba
```

---

## 💾 Problemas de Volúmenes

### Datos no persisten

```bash
# Verificar volúmenes nombrados
docker volume ls

# Inspeccionar volumen
docker volume inspect agente-cv_agente-data

# Verificar mounts
docker inspect agente-cv-app | grep -A 10 Mounts
```

### Volumen corrupto

```bash
# Backup primero!
docker run --rm -v agente-cv_agente-data:/data \
  -v $(pwd)/backup:/backup \
  alpine tar czf /backup/data.tar.gz /data

# Eliminar y recrear
docker-compose down -v
docker volume rm agente-cv_agente-data
docker-compose up -d
```

---

## ⚡ Performance Issues

### Alto uso de CPU

```bash
# Monitorear en tiempo real
docker stats

# Limitar CPU en docker-compose.yml
deploy:
  resources:
    limits:
      cpus: '2.0'

# Ver procesos dentro del contenedor
docker-compose exec agente-cv top
```

### Alto uso de Memoria

```bash
# Ver uso
docker stats --no-stream

# Limitar memoria
deploy:
  resources:
    limits:
      memory: 2G

# Liberar memoria
docker-compose restart agente-cv
```

### Contenedor muy lento

**Diagnóstico:**

```bash
# Ver I/O
docker stats --format "table {{.Container}}\t{{.BlockIO}}"

# Ver logs por performance
docker-compose logs --tail=100 | grep -i "slow\|timeout\|error"

# Profiling
docker-compose exec agente-cv python -m cProfile -s cumtime run_full_app.py
```

**Optimizaciones:**

```yaml
# En docker-compose.yml
services:
  agente-cv:
    # Usar tmpfs para directorios temporales
    tmpfs:
      - /tmp
      - /app/.cache

    # Aumentar shared memory
    shm_size: '2gb'
```

---

## 🔍 Comandos de Diagnóstico

### Información del Sistema

```bash
# Info de Docker
docker info
docker version

# Espacio en disco
docker system df -v

# Ver todas las imágenes
docker images

# Ver todos los contenedores (incluso detenidos)
docker ps -a
```

### Logs Detallados

```bash
# Ver todos los logs
docker-compose logs

# Logs de un servicio específico
docker-compose logs agente-cv

# Seguir logs en tiempo real
docker-compose logs -f

# Últimas N líneas
docker-compose logs --tail=100

# Desde un tiempo específico
docker-compose logs --since 2024-01-01T00:00:00

# Filtrar por palabra
docker-compose logs | grep ERROR
```

### Inspeccionar Contenedor

```bash
# Info completa
docker inspect agente-cv-app

# Estado
docker inspect agente-cv-app | grep -A 5 State

# Configuración de red
docker inspect agente-cv-app | grep -A 20 NetworkSettings

# Variables de entorno
docker inspect agente-cv-app | grep -A 50 Env

# Health check
docker inspect agente-cv-app | grep -A 10 Health
```

### Entrar al Contenedor

```bash
# Shell interactiva
docker-compose exec agente-cv bash

# Como root
docker-compose exec -u root agente-cv bash

# Ejecutar comando específico
docker-compose exec agente-cv ls -la /app
docker-compose exec agente-cv python --version
docker-compose exec agente-cv pip list

# Ver procesos
docker-compose exec agente-cv ps aux

# Ver uso de recursos
docker-compose exec agente-cv df -h
docker-compose exec agente-cv free -m
```

### Testing

```bash
# Health check manual
curl http://localhost:8000/health

# Test API
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'

# Test desde dentro del contenedor
docker-compose exec agente-cv python healthcheck.py

# Ejecutar tests
docker-compose exec agente-cv pytest
docker-compose exec agente-cv python -m pytest tests/
```

---

## 🆘 Resetear Todo (Última Opción)

**⚠️ CUIDADO: Esto eliminará todos los datos**

```bash
# 1. Detener todo
docker-compose down -v

# 2. Eliminar imágenes
docker rmi $(docker images -q agente-cv*)

# 3. Limpiar sistema
docker system prune -a -f --volumes

# 4. Eliminar directorios locales (backup primero!)
rm -rf logs/* storage/*

# 5. Reconstruir desde cero
docker-compose build --no-cache
docker-compose up -d
```

---

## 📞 ¿Aún tienes problemas?

1. **Verifica los logs primero:**

   ```bash
   docker-compose logs --tail=200 -f
   ```

2. **Revisa el healthcheck:**

   ```bash
   docker inspect agente-cv-app | grep -A 10 Health
   ```

3. **Prueba desde dentro del contenedor:**

   ```bash
   docker-compose exec agente-cv bash
   curl http://localhost:8000/health
   ```

4. **Busca issues similares:**

   - Revisa issues en el repositorio
   - Busca en Stack Overflow
   - Consulta la documentación oficial de Docker

5. **Crea un issue con:**
   - Output de `docker-compose logs`
   - Output de `docker inspect`
   - Tu `docker-compose.yml`
   - Tu sistema operativo y versión de Docker

---

**Última actualización:** Octubre 2025
