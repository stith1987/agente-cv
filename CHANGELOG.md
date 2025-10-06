# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [Unreleased]

### 🎯 En Desarrollo (develop)
- Implementación de estrategia de ramas Git
- Configuración de workflow de desarrollo

---

## [1.0.0] - 2025-10-06

### 🎉 Lanzamiento Inicial

#### ✨ Añadido (Added)
- Sistema agéntico multi-LLM con orquestador inteligente
- Agente clarificador para interacciones ambiguas
- Agente evaluador para validación de respuestas
- Agente de email con plantillas dinámicas
- Sistema RAG (Retrieval-Augmented Generation) con ChromaDB
- API REST con FastAPI
- Interfaz de usuario con Gradio
- Sistema de logging estructurado
- Configuración Docker completa con docker-compose
- Soporte para múltiples proveedores LLM:
  - OpenAI (GPT-4, GPT-3.5)
  - Anthropic (Claude)
  - Groq (Mixtral, Llama)
  - Google (Gemini)
  - Ollama (modelos locales)
- Base de datos SQLite para FAQs
- Sistema de tareas en segundo plano
- Healthcheck endpoints
- Documentación completa:
  - README.md principal
  - Documentación Docker
  - Arquitectura del sistema
  - Guías de contribución
  - Código de conducta

#### 🛠️ Arquitectura
- Patrón de diseño modular y extensible
- Separación de responsabilidades por agentes
- Sistema de dependencias inyectables
- Manejo robusto de errores
- Rate limiting y validaciones

#### 📦 Infraestructura
- Docker multi-stage builds
- Docker Compose para diferentes ambientes:
  - Desarrollo (docker-compose.dev.yml)
  - Producción (docker-compose.prod.yml)
  - Escalado (docker-compose.scaled.yml)
- Nginx como reverse proxy
- Health checks automáticos
- Scripts de inicio para Windows y Linux

#### 🧪 Testing
- Tests unitarios para componentes clave
- Tests de integración
- Validación de refactoring
- Tests de patrones agénticos

#### 📚 Documentación
- Arquitectura de software detallada
- Arquitectura de datos
- Arquitectura de prompts
- Arquitectura de solución
- Guías de Docker completas
- FAQs y troubleshooting
- Ejemplos de uso

---

## Tipos de Cambios

- `Added` (✨ Añadido): Para nuevas características
- `Changed` (🔄 Cambiado): Para cambios en funcionalidad existente
- `Deprecated` (⚠️ Obsoleto): Para características que serán removidas
- `Removed` (🗑️ Removido): Para características removidas
- `Fixed` (🐛 Corregido): Para corrección de bugs
- `Security` (🔒 Seguridad): Para vulnerabilidades corregidas

---

## [Template para Nuevas Versiones]

## [X.Y.Z] - YYYY-MM-DD

### ✨ Añadido (Added)
- Nueva característica 1
- Nueva característica 2

### 🔄 Cambiado (Changed)
- Cambio en comportamiento existente

### ⚠️ Obsoleto (Deprecated)
- Característica que será removida

### 🗑️ Removido (Removed)
- Característica removida

### 🐛 Corregido (Fixed)
- Bug fix 1
- Bug fix 2

### 🔒 Seguridad (Security)
- Parche de seguridad

---

## Links de Comparación

[Unreleased]: https://github.com/stith1987/agente-cv/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/stith1987/agente-cv/releases/tag/v1.0.0
