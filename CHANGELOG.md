# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [Unreleased]

### 🎯 En Desarrollo (develop)

- Implementación de estrategia de ramas Git
- Configuración de workflow de desarrollo

---

## [1.1.1] - 2025-10-06

### 📋 Documentación

#### ✨ Añadido (Added)

- **Architecture Decision Records (ADR)** - Documento completo en `docs/ADR.md`
  - ADR-001: Uso de RAG para generación de respuestas
  - ADR-002: FastAPI como framework de API
  - ADR-003: ChromaDB como vector database
  - ADR-004: Arquitectura modular con patrón orquestador
  - ADR-005: Sistema Multi-LLM plug-and-play
  - ADR-006: Git Flow como estrategia de ramas
  - ADR-007: Docker y Docker Compose para despliegue
  - ADR-008: Gradio para interfaz de usuario
  - ADR-009: SQLite para FAQs estructuradas
  - ADR-010: Refactorización a arquitectura limpia
- **Índice Maestro de Documentación** - `docs/README.md`
  - Organización por categorías (Arquitectura, Desarrollo, Docker, Git)
  - Roadmap de lectura para diferentes roles (Junior, Senior, Arquitecto)
  - Enlaces a todas las decisiones arquitectónicas
  - Métricas del proyecto y herramientas disponibles
  - Sección de ayuda y troubleshooting

#### 🔄 Cambiado (Changed)

- **README.md** - Añadida sección "🏛️ Decisiones de Arquitectura" con enlaces a ADR

#### 📊 Impacto

- ✅ Documentación de decisiones arquitectónicas centralizada y justificada
- ✅ Historia completa de por qué se tomaron decisiones técnicas
- ✅ Referencia rápida para nuevos desarrolladores
- ✅ Base sólida para futuras decisiones arquitectónicas
- ✅ Transparencia en trade-offs y alternativas consideradas

---

## [1.1.0] - 2025-10-06

### 🎉 Multi-LLM Plug-and-Play

#### ✨ Añadido (Added)

- **Multi-LLM Client**: Cliente unificado compatible con OpenAI API
  - Soporte para OpenAI, DeepSeek, Groq, Gemini, Ollama, Anthropic
  - Configuración plug-and-play vía `base_url` y `api_key`
  - Cliente síncrono y asíncrono
- **Sistema de Ensemble**: Invocación paralela de múltiples modelos
  - Generación asíncrona simultánea
  - Selección del mejor output por criterio
  - Combinación inteligente de respuestas
- **Configuración extendida**:
  - `OpenAIConfig` ahora soporta `base_url` y `provider`
  - Variables de entorno: `LLM_PROVIDER`, `OPENAI_BASE_URL`
- **Documentación completa**:
  - Guía Multi-LLM (`docs/MULTI_LLM_GUIDE.md`)
  - Demo funcional (`examples/multi_llm_demo.py`)
  - Comparativas de proveedores y precios
  - Ejemplos de configuración para cada proveedor

#### 🔄 Cambiado (Changed)

- **CVOrchestrator**: Ahora usa `MultiLLMClient` internamente
  - Mantiene retrocompatibilidad con `openai_client`
  - Soporte transparente para proveedores alternativos
- **AgentConfig**: Método `from_env()` actualizado para leer nuevas variables

#### 📚 Documentación

- ✅ Guía completa de Multi-LLM con ejemplos
- ✅ Comparativa de performance y costos
- ✅ Casos de uso por proveedor
- ✅ Troubleshooting específico por proveedor

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
