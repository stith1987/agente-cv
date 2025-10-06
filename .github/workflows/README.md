# 🔄 CI/CD con GitHub Actions para agente-cv

## Descripción

Este workflow de GitHub Actions automatiza:

- ✅ Build de imágenes Docker
- ✅ Tests de la aplicación
- ✅ Escaneo de seguridad
- ✅ Push al Container Registry
- ✅ Deployment (opcional)

## 📁 Ubicación

`.github/workflows/docker-ci.yml`

## 🚀 Triggers

El workflow se ejecuta automáticamente en:

- **Push** a `main` o `develop`
- **Pull Requests** hacia `main`
- **Manualmente** desde la pestaña Actions

## 🔐 Configuración

### 1. Secrets Requeridos

En tu repositorio de GitHub, ve a `Settings > Secrets and variables > Actions` y agrega:

```
OPENAI_API_KEY          # Para tests
ANTHROPIC_API_KEY       # Para tests
GROQ_API_KEY           # Para tests
DOCKER_USERNAME         # Si usas Docker Hub
DOCKER_PASSWORD         # Si usas Docker Hub
```

### 2. GitHub Container Registry

El workflow ya está configurado para usar `ghcr.io` (GitHub Container Registry).

**Permisos necesarios:**

- En `Settings > Actions > General > Workflow permissions`
- Selecciona "Read and write permissions"

## 📊 Jobs del Pipeline

### 1. Build & Test

```yaml
- Checkout del código
- Setup de Docker Buildx
- Login al registry
- Build de la imagen
- Tests básicos
- Push al registry (solo en main/develop)
```

### 2. Security Scan

```yaml
- Escaneo con Trivy
- Reporte de vulnerabilidades
- Upload a GitHub Security
```

## 🏷️ Tags de Imágenes

Las imágenes se tagean automáticamente:

- `ghcr.io/stith1987/agente-cv:main` - Última versión en main
- `ghcr.io/stith1987/agente-cv:develop` - Última versión en develop
- `ghcr.io/stith1987/agente-cv:pr-123` - Para PRs
- `ghcr.io/stith1987/agente-cv:sha-abc123` - Por commit SHA

## 🔍 Ver Resultados

1. Ve a la pestaña **Actions** en tu repositorio
2. Selecciona el workflow "Docker CI/CD"
3. Click en el run más reciente
4. Revisa logs de cada job

## 📦 Usar la Imagen

### Pull desde GitHub Container Registry

```bash
# Login (solo primera vez)
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Pull
docker pull ghcr.io/stith1987/agente-cv:main

# Run
docker run -d \
  -p 8000:8000 \
  -p 7860:7860 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  ghcr.io/stith1987/agente-cv:main
```

### Actualizar docker-compose.yml

```yaml
services:
  agente-cv:
    image: ghcr.io/stith1987/agente-cv:main
    # resto de la configuración...
```

## 🔧 Personalización

### Cambiar el Registry

Para usar Docker Hub en lugar de ghcr.io:

```yaml
env:
  REGISTRY: docker.io
  IMAGE_NAME: tu-usuario/agente-cv
```

### Agregar Tests

Edita el workflow para incluir tus tests:

```yaml
- name: Run tests
  run: |
    docker-compose run --rm agente-cv pytest tests/
```

### Deploy Automático

Agrega un job de deployment:

```yaml
deploy:
  needs: build
  if: github.ref == 'refs/heads/main'
  runs-on: ubuntu-latest
  steps:
    - name: Deploy to production
      run: |
        # Comandos de deployment
        # Ejemplo: ssh, kubectl, docker-compose, etc.
```

## 🛡️ Security Best Practices

1. **Nunca** hagas commit de secretos
2. Usa GitHub Secrets para credenciales
3. Revisa los reportes de Trivy
4. Mantén las dependencias actualizadas
5. Usa tags específicos, no `latest`

## 📈 Monitoreo

### Ver imágenes publicadas

```bash
# En GitHub Packages
https://github.com/stith1987?tab=packages

# O con API
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/users/stith1987/packages/container/agente-cv/versions
```

### Ver reportes de seguridad

```bash
# En GitHub Security
https://github.com/stith1987/agente-cv/security/code-scanning
```

## 🐛 Troubleshooting

### Error: Permission denied

**Problema**: El workflow no puede push al registry.

**Solución**:

1. Ve a `Settings > Actions > General`
2. En "Workflow permissions", selecciona "Read and write permissions"
3. Click "Save"

### Error: Tests failing

**Problema**: Los tests fallan en CI pero funcionan localmente.

**Solución**:

1. Verifica que los secretos estén configurados
2. Revisa los logs del workflow
3. Ejecuta localmente con:
   ```bash
   docker-compose run --rm agente-cv pytest
   ```

### Error: Image too large

**Problema**: La imagen es muy grande.

**Solución**:

1. Optimiza el Dockerfile (ver DOCKER_BEST_PRACTICES.md)
2. Usa multi-stage builds
3. Limpia archivos innecesarios

## 📚 Recursos

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Trivy Scanner](https://github.com/aquasecurity/trivy)
- [Docker Best Practices](DOCKER_BEST_PRACTICES.md)

## 🎯 Próximos Pasos

1. ✅ Workflow básico implementado
2. ⬜ Agregar tests de integración
3. ⬜ Configurar deployment automático
4. ⬜ Agregar notificaciones (Slack, Discord)
5. ⬜ Implementar rolling updates
6. ⬜ Agregar smoke tests post-deploy

---

**💡 Tip**: Revisa los logs de cada run para identificar problemas rápidamente.
