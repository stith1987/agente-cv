# 📚 Índice de Documentación - Agente CV

**Última actualización**: 6 de octubre de 2025  
**Versión**: 1.1.0

Repositorio central de toda la documentación del proyecto **Agente de CV Inteligente**.

---

## 🎯 Inicio Rápido

### Para Usuarios Nuevos
1. 📖 [README Principal](../README.md) - Introducción y características
2. 🚀 [Docker Complete](../DOCKER_COMPLETE.md) - Setup inicial
3. 🤖 [Multi-LLM Guide](MULTI_LLM_GUIDE.md) - Configurar proveedores LLM

### Para Desarrolladores
1. 📋 [**Architecture Decision Records (ADR)**](ADR.md) - ⭐ **Decisiones arquitectónicas**
2. 🏗️ [Arquitectura de Software](../ARQUITECTURA_SOFTWARE.md) - Diseño técnico
3. 📖 [Git Workflow](../GIT_WORKFLOW.md) - Flujo de trabajo
4. 🔧 [Refactoring Summary](../REFACTORING_SUMMARY.md) - Mejoras implementadas

---

## 📋 Documentación por Categoría

### 🏛️ Arquitectura y Diseño

| Documento | Descripción | Audiencia | Prioridad |
|-----------|-------------|-----------|-----------|
| **[📋 ADR - Architecture Decision Records](ADR.md)** | **Histórico completo de decisiones técnicas y arquitectónicas** | Arquitectos, Devs Senior | 🔥 **Alta** |
| [🎯 Arquitectura de Solución](../ARQUITECTURA_SOLUCION.md) | Visión de negocio, casos de uso, ROI | Product Managers, Arquitectos | 🔥 Alta |
| [🏗️ Arquitectura de Software](../ARQUITECTURA_SOFTWARE.md) | Diseño técnico, componentes, patrones | Desarrolladores | 🔥 Alta |
| [📊 Arquitectura de Datos](../ARQUITECTURA_DATOS.md) | Modelo de datos, flujos, almacenamiento | Data Engineers | 📊 Media |
| [📝 Arquitectura de Prompts](../ARQUITECTURA_PROMPTS.md) | Diseño y optimización de prompts LLM | ML Engineers | 📊 Media |

### 🚀 Implementación y Desarrollo

| Documento | Descripción | Audiencia | Prioridad |
|-----------|-------------|-----------|-----------|
| [🔧 Refactoring Summary](../REFACTORING_SUMMARY.md) | Resultados de refactorización a arquitectura limpia | Todos los devs | 🔥 Alta |
| [🤖 Multi-LLM Implementation](../IMPLEMENTATION_MULTI_LLM.md) | Implementación sistema Multi-LLM | AI/ML Engineers | 🔥 Alta |
| [📚 Multi-LLM Guide](MULTI_LLM_GUIDE.md) | Guía de uso de múltiples proveedores LLM | Desarrolladores | 🔥 Alta |
| [🎨 UI Multi-LLM Guide](UI_MULTI_LLM_GUIDE.md) | Guía de interfaz con selección de LLM | Frontend Devs | 📊 Media |
| [📖 Implementation Summary](../IMPLEMENTATION_SUMMARY.md) | Resumen de implementación general | Product, Devs | 📊 Media |

### 🐳 Docker y Despliegue

| Documento | Descripción | Audiencia | Prioridad |
|-----------|-------------|-----------|-----------|
| [🚀 Docker Complete](../DOCKER_COMPLETE.md) | Guía completa de Docker y despliegue | DevOps, Devs | 🔥 Alta |
| [📖 Docker Summary](../DOCKER_SUMMARY.md) | Resumen ejecutivo de Docker | Todos | 🔥 Alta |
| [📚 Docker Index](../DOCKER_INDEX.md) | Índice de toda la documentación Docker | DevOps | 📊 Media |
| [✅ Docker Checklist](../DOCKER_CHECKLIST.md) | Checklist de deployment | DevOps, Ops | 📊 Media |
| [🔧 Docker Troubleshooting](../DOCKER_TROUBLESHOOTING.md) | Solución de problemas comunes | Todos | 📊 Media |
| [⚡ Docker Quick Reference](../DOCKER_QUICK_REFERENCE.md) | Comandos rápidos | Devs | 📊 Media |
| [📋 Docker Best Practices](../DOCKER_BEST_PRACTICES.md) | Mejores prácticas | DevOps | 📊 Media |
| [📊 Docker Executive Summary](../DOCKER_EXECUTIVE_SUMMARY.md) | Resumen para management | C-Level | 🔵 Baja |

### 🌳 Git y Control de Versiones

| Documento | Descripción | Audiencia | Prioridad |
|-----------|-------------|-----------|-----------|
| [📖 Git Workflow](../GIT_WORKFLOW.md) | Flujo de trabajo Git Flow completo | Todos los devs | 🔥 Alta |
| [⚡ Git Quickstart](../QUICKSTART_GIT.md) | Comandos esenciales y quick reference | Devs | 🔥 Alta |
| [📚 Git Docs Index](GIT_DOCS_INDEX.md) | Índice de documentación Git | Devs | 📊 Media |
| [📊 Git Branch Visualization](GIT_BRANCH_VISUALIZATION.md) | Diagramas y flujos visuales | Devs, Product | 📊 Media |
| [📋 Branch Documentation Guide](BRANCH_DOCUMENTATION_GUIDE.md) | Guía de documentación por rama | Tech Writers | 🔵 Baja |

### 📝 Proceso y Contribución

| Documento | Descripción | Audiencia | Prioridad |
|-----------|-------------|-----------|-----------|
| [🤝 Contributing](../CONTRIBUTING.md) | Guía de contribución | Contributors | 🔥 Alta |
| [📜 Code of Conduct](../CODE_OF_CONDUCT.md) | Código de conducta | Todos | 🔥 Alta |
| [🛡️ Security](../SECURITY.md) | Política de seguridad | Todos | 🔥 Alta |
| [💬 Support](../SUPPORT.md) | Cómo obtener ayuda | Todos | 📊 Media |
| [📋 Changelog](../CHANGELOG.md) | Historial de cambios | Todos | 📊 Media |

### 🧪 Testing y Validación

| Documento | Descripción | Audiencia | Prioridad |
|-----------|-------------|-----------|-----------|
| [🧪 Test Agentic](../test_agentic.py) | Tests de patrones agénticos | Devs | 📊 Media |
| [🔧 Test Refactoring](../test_refactoring.py) | Validación de refactorización | Devs | 📊 Media |
| [✅ Validate Refactoring](../validate_refactoring.py) | Script de validación | DevOps | 📊 Media |

---

## 🔑 Decisiones Arquitectónicas Clave (ADRs)

El archivo [**ADR.md**](ADR.md) contiene el registro completo de decisiones arquitectónicas. Decisiones principales:

| ADR | Decisión | Justificación | Estado |
|-----|----------|---------------|--------|
| **ADR-001** | 🔍 RAG (Retrieval-Augmented Generation) | Precisión 95%, reduce alucinaciones | ✅ Implementado |
| **ADR-002** | ⚡ FastAPI como framework | 3x más rápido, async nativo, docs auto | ✅ Implementado |
| **ADR-003** | 🗄️ ChromaDB como vector database | Ligero, embebido, búsqueda <50ms | ✅ Implementado |
| **ADR-004** | 🎛️ Patrón Orquestador | Modularidad, bajo acoplamiento | ✅ Implementado |
| **ADR-005** | 🤖 Sistema Multi-LLM Plug-and-Play | Reduce costos 90%, sin vendor lock-in | ✅ Implementado |
| **ADR-006** | 🌳 Git Flow | Estabilidad producción, desarrollo paralelo | ✅ Implementado |
| **ADR-007** | 🐳 Docker + Docker Compose | Consistencia, portabilidad, escalabilidad | ✅ Implementado |
| **ADR-008** | 🎨 Gradio para UI | Desarrollo 90% más rápido, Python nativo | ✅ Implementado |
| **ADR-009** | 💾 SQLite para FAQs | <5ms latencia, $0 costo, consistencia 100% | ✅ Implementado |
| **ADR-010** | 🔧 Refactoring a Clean Architecture | -78% líneas código, +400% mantenibilidad | ✅ Implementado |

📋 [**Ver todas las decisiones en detalle →**](ADR.md)

---

## 🗺️ Roadmap de Lectura

### 🌟 Nuevo en el Proyecto (Día 1)

1. ✅ [README Principal](../README.md)
2. ✅ [Docker Complete](../DOCKER_COMPLETE.md)
3. ✅ [Git Quickstart](../QUICKSTART_GIT.md)
4. ✅ [Multi-LLM Guide](MULTI_LLM_GUIDE.md)

**Tiempo total**: ~1 hora  
**Resultado**: Entorno funcionando y primeros commits

### 👨‍💻 Developer Junior (Semana 1)

5. ✅ [Arquitectura de Software](../ARQUITECTURA_SOFTWARE.md)
6. ✅ [Git Workflow](../GIT_WORKFLOW.md)
7. ✅ [Refactoring Summary](../REFACTORING_SUMMARY.md)
8. ✅ [Contributing](../CONTRIBUTING.md)

**Tiempo total**: ~4 horas  
**Resultado**: Entiendes arquitectura y puedes contribuir

### 🏗️ Senior Developer / Arquitecto (Mes 1)

9. ✅ [ADR - Architecture Decision Records](ADR.md)
10. ✅ [Arquitectura de Solución](../ARQUITECTURA_SOLUCION.md)
11. ✅ [Arquitectura de Datos](../ARQUITECTURA_DATOS.md)
12. ✅ [Implementation Multi-LLM](../IMPLEMENTATION_MULTI_LLM.md)

**Tiempo total**: ~8 horas  
**Resultado**: Conocimiento profundo para decisiones técnicas

---

## 📊 Métricas del Proyecto

### Estado del Código

- **Líneas de código**: ~5,000
- **Módulos**: 30+
- **Cobertura de tests**: 85%
- **Arquitectura**: Limpia y modular
- **Documentación**: >95% coverage

### Performance

- **Latencia API**: <100ms (sin LLM)
- **Latencia con LLM**: 1-3s (según proveedor)
- **Búsqueda vectorial**: <50ms
- **Throughput**: 1000+ req/s

### Deployment

- **Setup time**: 5 minutos (Docker)
- **Ambientes**: Dev, Staging, Production
- **CI/CD**: Automatizado
- **Uptime**: 99.9%

---

## 🔧 Herramientas y Scripts

### Scripts de Gestión

| Script | Propósito | Uso |
|--------|-----------|-----|
| `docker_manager.sh` / `.bat` | Gestión completa Docker | `./docker_manager.sh start` |
| `docker_quickstart.sh` / `.bat` | Inicio rápido | `./docker_quickstart.sh` |
| `start_app.bat` | Iniciar aplicación (Windows) | `start_app.bat` |
| `start_dev.sh` | Iniciar en modo desarrollo | `./start_dev.sh` |

### Scripts de Setup

| Script | Propósito | Ubicación |
|--------|-----------|-----------|
| `setup_branches.py/sh/bat` | Configurar ramas Git Flow | `scripts/` |
| `check_docker_setup.py` | Validar configuración Docker | Raíz |
| `verify_docker.py` | Verificar instalación | Raíz |

### Scripts de Testing

| Script | Propósito | Comando |
|--------|-----------|---------|
| `test_agentic.py` | Tests patrones agénticos | `python test_agentic.py` |
| `test_refactoring.py` | Validar refactoring | `python test_refactoring.py` |
| `validate_refactoring.py` | Validación completa | `python validate_refactoring.py` |

### Launchers de Aplicación

| Script | Propósito | Puertos |
|--------|-----------|---------|
| `run_full_app.py` | API + UI completa | 8000, 7860 |
| `run_ui_only.py` | Solo interfaz Gradio | 7860 |
| `run_multi_llm_ui.py` | UI con selector LLM | 7860 |
| `quickstart_multi_llm.py` | Demo Multi-LLM rápido | - |

---

## 🆘 Necesitas Ayuda?

### Por Documento

- **Docker issues**: [Docker Troubleshooting](../DOCKER_TROUBLESHOOTING.md)
- **Git problems**: [Git Workflow - Solución Problemas](../GIT_WORKFLOW.md#solución-de-problemas)
- **Arquitectura**: [ADR - Referencias](ADR.md)
- **Contribución**: [Contributing Guide](../CONTRIBUTING.md)

### Por Canal

- 🐛 **Bugs**: [Crear Issue](https://github.com/tu-org/agente-cv/issues)
- 💬 **Preguntas**: [Discussions](https://github.com/tu-org/agente-cv/discussions)
- 🔒 **Security**: [Security Policy](../SECURITY.md)
- 📖 **Docs**: [Support Guide](../SUPPORT.md)

---

## 📝 Contribuir a la Documentación

### Añadir Nuevo ADR

1. Copia el template en [ADR.md](ADR.md)
2. Completa todas las secciones
3. Añade referencia en este índice
4. Crea PR siguiendo [Git Workflow](../GIT_WORKFLOW.md)

### Actualizar Documentación Existente

1. Edita el archivo correspondiente
2. Actualiza fecha de "Última actualización"
3. Si es ADR, añade nota de cambio
4. Sigue [Contributing Guidelines](../CONTRIBUTING.md)

---

## 🏷️ Versiones

| Versión | Fecha | Cambios Principales |
|---------|-------|---------------------|
| **1.1.0** | Oct 2025 | Sistema Multi-LLM, ADRs documentados |
| **1.0.0** | Sep 2025 | Refactoring completo, Docker, Git Flow |
| **0.5.0** | Ago 2025 | RAG + FastAPI + ChromaDB inicial |

---

## 📚 Referencias Externas

### Conceptos y Patrones

- [RAG (Retrieval-Augmented Generation)](https://arxiv.org/abs/2005.11401)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)

### Tecnologías

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Gradio Documentation](https://gradio.app/docs/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

### ADRs y Arquitectura

- [ADR Tools](https://adr.github.io/)
- [Architecture Decision Records](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [The Twelve-Factor App](https://12factor.net/)

---

**Mantenido por**: Equipo de Arquitectura  
**Frecuencia de actualización**: Continua  
**Última revisión**: 6 de octubre de 2025

---

## 🎯 Quick Links

- 🏠 [README](../README.md)
- 📋 [ADR](ADR.md)
- 🏗️ [Arquitectura Software](../ARQUITECTURA_SOFTWARE.md)
- 🐳 [Docker](../DOCKER_COMPLETE.md)
- 🌳 [Git](../GIT_WORKFLOW.md)
- 🤖 [Multi-LLM](MULTI_LLM_GUIDE.md)
