# 🤖 Agente de CV Inteligente

Un sistema de inteligencia artificial conversacional avanzado que utiliza **RAG (Retrieval-Augmented Generation)** y herramientas especializadas para responder preguntas inteligentes sobre experiencia profesional, proyectos y habilidades técnicas.

## ✨ Características Principales

- 🔍 **RAG Semántico**: Búsqueda inteligente con ChromaDB y sentence-transformers
- 📊 **Base de FAQs**: Sistema SQLite para preguntas frecuentes estructuradas
- 🧠 **Evaluación Automática**: LLM evaluador con auto-crítica y mejora continua
- 📬 **Notificaciones**: Integración con Pushover para alertas en tiempo real
- 🌐 **API REST**: FastAPI con documentación automática (OpenAPI/Swagger)
- 💻 **Interfaz Web**: UI moderna con Gradio para interacción visual
- 🎛️ **Orquestador Inteligente**: Routing automático de consultas a la herramienta óptima
- ⚡ **Ejecución Flexible**: Scripts de inicio para API sola o sistema completo
- 🐳 **Docker Ready**: Contenerización completa con Docker y Docker Compose

## 🐳 Inicio Rápido con Docker

La forma más rápida de empezar:

```bash
# 1. Configurar variables de entorno
cp .env.example .env
# Edita .env con tus API keys

# 2. Iniciar con Docker
docker-compose up -d

# 3. Acceder a la aplicación
# API: http://localhost:8000
# UI:  http://localhost:7860
```

📦 **Documentación Docker:**

- 🚀 [Inicio Rápido](DOCKER_COMPLETE.md)
- 📖 [Guía Completa](DOCKER_SUMMARY.md)
- 📚 [Índice Completo](DOCKER_INDEX.md)

## 📁 Estructura del Proyecto

```
├── README.md                     # 📖 Este archivo
├── requirements.txt              # 📦 Dependencias Python
├── run_full_app.py              # 🚀 Launcher: API + UI
├── run_ui_only.py               # 🎨 Launcher: Solo UI
├── start_app.bat                # 🖥️ Script Windows
├── test_agentic.py              # 🧪 Test de patrones agénticos
├── test_refactoring.py          # 🔧 Validación refactoring
│
├── 📚 data/                     # Conocimiento base
│   ├── cv.md                    # CV personal completo
│   ├── proyectos/               # Proyectos específicos
│   │   ├── 01-banca-digital.md
│   │   └── 02-arch-enterprise.md
│   └── recortes/                # Artículos y experiencias
│       ├── articulo-fintech-microservices.md
│       ├── devops-days-2023.md
│       └── workshop-kubernetes-2022.md
│
├── 🧠 agent/                    # Motor de IA
│   ├── orchestrator.py          # Lógica central de routing
│   ├── evaluator.py             # Sistema de evaluación
│   ├── clarifier.py             # Clarificación de consultas
│   ├── email_agent.py           # Agente de emails
│   └── prompts.py               # Templates de prompts
│
├── 🌐 api/                      # Interfaces web
│   ├── app.py                   # FastAPI principal (refactorizado)
│   ├── ui_gradio.py             # Interfaz Gradio
│   ├── dependencies.py          # Inyección de dependencias
│   ├── exceptions.py            # Manejo de errores
│   ├── background_tasks.py      # Tareas asíncronas
│   ├── models/                  # Modelos Pydantic
│   │   ├── requests.py
│   │   └── responses.py
│   └── routes/                  # Endpoints organizados
│       ├── chat.py
│       ├── health.py
│       ├── stats.py
│       └── notifications.py
│
├── 🔍 rag/                      # Sistema RAG
│   ├── ingest.py                # Indexación de documentos
│   └── retriever.py             # Búsqueda semántica
│
├── 🛠️ tools/                   # Herramientas especializadas
│   ├── faq_sql.py               # FAQ con SQLite
│   ├── notify.py                # Notificaciones Pushover
│   └── tool_schemas.py          # Esquemas JSON
│
├── 💾 storage/                  # Bases de datos
│   ├── vectordb/                # ChromaDB (vector embeddings)
│   └── sqlite/                  # SQLite (FAQs estructuradas)
│       └── faq.db
│
└── 📄 examples/                 # Ejemplos y demos
    └── agentic_patterns_demo.py
```

## 🛠️ Instalación

1. **Clonar el repositorio**

   ```bash
   git clone <tu-repositorio>
   cd agente-cv
   ```

2. **Crear entorno virtual**

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**

   ```bash
   cp .env.example .env
   # Editar .env con tus claves API
   ```

5. **Inicializar la base de datos**
   ```bash
   python -m rag.ingest
   ```

## � Ejecución con Docker (Recomendado)

La forma más rápida y sencilla de ejecutar la aplicación es usando Docker:

### Inicio Rápido

```bash
# 1. Configurar variables de entorno
cp .env.example .env
# Edita .env con tus claves API

# 2. Construir y ejecutar
docker-compose up -d

# 3. Ver logs
docker-compose logs -f
```

**Servicios disponibles:**

- 🌐 **API REST**: http://localhost:8000 (con `/docs`)
- 💻 **Interfaz Web**: http://localhost:7860

### Comandos Útiles

```bash
# Ver estado
docker-compose ps

# Detener servicios
docker-compose down

# Reconstruir
docker-compose build --no-cache

# Ver logs
docker-compose logs -f agente-cv
```

### Scripts de Gestión

**Windows:**

```cmd
docker_manager.bat up      # Iniciar
docker_manager.bat logs    # Ver logs
docker_manager.bat down    # Detener
```

**Linux/Mac:**

```bash
./docker_manager.sh up
./docker_manager.sh logs
./docker_manager.sh down
```

**Con Make:**

```bash
make up        # Iniciar
make logs      # Ver logs
make down      # Detener
make status    # Ver estado
make shell     # Abrir terminal en contenedor
```

📖 **Documentación completa**: Ver [README_DOCKER.md](README_DOCKER.md)

## �🚦 Formas de Ejecución (Sin Docker)

### ⚡ Opción 1: Sistema Completo (Recomendado)

```bash
# Activa el entorno virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Ejecuta API + UI simultáneamente
python run_full_app.py
```

**Servicios disponibles:**

- 🌐 **API REST**: `http://localhost:8000` (con documentación en `/docs`)
- 💻 **Interfaz Web**: `http://localhost:7860`

### 🎨 Opción 2: Solo Interfaz Web

```bash
python run_ui_only.py
```

### 🖥️ Opción 3: Script Windows (Automático)

```cmd
start_app.bat
```

### 🔧 Opción 4: Solo API (Desarrollo)

```bash
python api\app.py
```

### 📡 Uso de la API

**Endpoint principal:**

```bash
POST http://localhost:8000/chat
Content-Type: application/json

{
  "message": "¿Cuáles son mis principales proyectos de banca digital?",
  "session_id": "user123"
}
```

**Otros endpoints:**

- `GET /health` - Estado del sistema
- `GET /stats` - Estadísticas de uso
- `POST /notifications/test` - Test de notificaciones

### 💻 Uso Programático

```python
from agent.orchestrator import CVOrchestrator

# Inicializar orquestador
orchestrator = CVOrchestrator()

# Procesar consulta
response = orchestrator.process_query(
    "¿Qué experiencia tengo en arquitectura empresarial?"
)

print(f"Respuesta: {response['response']}")
print(f"Herramientas usadas: {response['tools_used']}")
print(f"Confianza: {response['confidence']}")
```

## ⚙️ Configuración

### Variables de Entorno Principales

Crea un archivo `.env` en la raíz del proyecto:

```env
# OpenAI Configuration (REQUERIDO)
OPENAI_API_KEY=sk-tu_clave_aqui
OPENAI_MODEL=gpt-3.5-turbo  # o gpt-4

# Base de Datos
VECTORDB_PATH=./storage/vectordb/
SQLITE_DB_PATH=./storage/sqlite/faq.db

# RAG Configuration
TOP_K_RESULTS=5
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Notificaciones (OPCIONAL)
PUSHOVER_TOKEN=tu_token_pushover
PUSHOVER_USER_KEY=tu_user_key

# Servidor
PORT=8000
GRADIO_PORT=7860
API_BASE_URL=http://localhost:8000

# Desarrollo
PYTHONPATH=.
LOG_LEVEL=INFO
```

### 🔑 Variables Críticas

| Variable         | Requerido | Descripción         | Default                   |
| ---------------- | --------- | ------------------- | ------------------------- |
| `OPENAI_API_KEY` | ✅ **Sí** | Clave API de OpenAI | -                         |
| `OPENAI_MODEL`   | ❌ No     | Modelo GPT a usar   | `gpt-3.5-turbo`           |
| `VECTORDB_PATH`  | ❌ No     | Ruta ChromaDB       | `./storage/vectordb/`     |
| `SQLITE_DB_PATH` | ❌ No     | Ruta base FAQs      | `./storage/sqlite/faq.db` |
| `TOP_K_RESULTS`  | ❌ No     | Resultados RAG      | `5`                       |
| `PORT`           | ❌ No     | Puerto API          | `8000`                    |
| `GRADIO_PORT`    | ❌ No     | Puerto UI           | `7860`                    |

### Personalización

1. **Agregar documentos**: Coloca tus archivos MD en `data/`
2. **FAQs**: Edita la base SQLite en `storage/sqlite/faq.db`
3. **Prompts**: Personaliza en `agent/prompts.py`
4. **Herramientas**: Añade nuevas tools en `tools/`

## 📊 Componentes Técnicos

### 🔍 RAG (Retrieval-Augmented Generation)

- **Ingest**: Procesa archivos MD con metadatos y chunking inteligente
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` para vectorización
- **Vector DB**: ChromaDB para almacenamiento y búsqueda semántica
- **Retriever**: Top-K similarity search con filtros contextuales

### 🛠️ Sistema de Herramientas

- **FAQ SQL**: SQLAlchemy + SQLite para consultas estructuradas
- **Notificaciones**: Pushover API para alertas en tiempo real
- **Tool Schemas**: Pydantic para validación de entrada/salida
- **Background Tasks**: FastAPI para procesamiento asíncrono

### 🧠 Motor de IA

- **Orquestador**: Lógica de routing con GPT-3.5-turbo/GPT-4
- **Evaluador**: Sistema de auto-evaluación y mejora continua
- **Clarificador**: Procesamiento de consultas ambiguas
- **Email Agent**: Generación de emails profesionales
- **Prompts**: Templates especializados por tipo de consulta

### 🌐 APIs y UI

- **FastAPI**: API REST con documentación automática OpenAPI
- **Gradio**: Interfaz web moderna y responsiva
- **CORS**: Configurado para integraciones externas
- **Health Checks**: Monitoreo de estado de componentes

## 🧪 Testing y Validación

### Scripts de Prueba Incluidos

```bash
# Test completo de patrones agénticos
python test_agentic.py

# Validación post-refactoring
python test_refactoring.py
```

### Pruebas Manuales

```bash
# Test de la API
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola, cuéntame sobre tu experiencia", "session_id": "test"}'

# Health check
curl http://localhost:8000/health

# Documentación interactiva
# Abrir: http://localhost:8000/docs
```

### 🔍 Debugging

```bash
# Verificar base de datos vectorial
python -c "from rag.retriever import RAGRetriever; r = RAGRetriever(); print(f'Documentos indexados: {r.get_collection_size()}')"

# Test de herramientas individualmente
python -c "from tools.faq_sql import get_faq_answer; print(get_faq_answer('experiencia'))"
```

## � Roadmap y Mejoras Futuras

### 🔥 En Desarrollo

- [ ] Dashboard de analytics y métricas de uso
- [ ] Integración con calendarios (Google Calendar)
- [ ] Export de respuestas a PDF/Word
- [ ] Plugin para LinkedIn y redes sociales

### 🔮 Planificado

- [ ] Soporte multilingüe (ES/EN)
- [ ] Integración con más LLMs (Claude, Gemini)
- [ ] Chat persistente con historial
- [ ] API webhooks para integraciones

### 🌱 Ideas Futuras

- [ ] Generación automática de propuestas
- [ ] Integración con CRM (HubSpot, Salesforce)
- [ ] Análisis de sentimientos en conversaciones
- [ ] Modo voice-to-text para consultas por voz

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

---

## 📚 Documentación Docker

### Guías Principales

- 📦 **[Resumen de Docker](DOCKER_SUMMARY.md)** - Overview completo de la implementación
- 📖 **[Guía de Usuario](README_DOCKER.md)** - Instrucciones detalladas de uso
- 🚀 **[Referencia Rápida](DOCKER_QUICK_REFERENCE.md)** - Comandos más usados

### Recursos Avanzados

- 🏆 **[Mejores Prácticas](DOCKER_BEST_PRACTICES.md)** - Optimización y seguridad
- 🔧 **[Troubleshooting](DOCKER_TROUBLESHOOTING.md)** - Resolución de problemas
- 🛠️ **Scripts de Gestión**
  - `docker_manager.bat` / `docker_manager.sh` - Gestión de contenedores
  - `docker_quickstart.bat` / `docker_quickstart.sh` - Inicio interactivo
  - `Makefile` - Comandos make
  - `verify_docker.py` - Verificación pre-deployment

---

**✨ Hecho con ❤️ por [Eduardo](https://github.com/stith1987)**

## � Autor y Contacto

**Eduardo** - Desarrollador de IA y Arquitecto de Software  
📧 Email: [Contacto directo vía GitHub](https://github.com/stith1987/agente-cv/issues)  
🔗 Repositorio: [`stith1987/agente-cv`](https://github.com/stith1987/agente-cv)

---

## 🚀 ¿Te Gusta el Proyecto?

Si encuentras útil este agente de CV:

- ⭐ **Dale una estrella** al repositorio
- 🐛 **Reporta bugs** en [Issues](https://github.com/stith1987/agente-cv/issues)
- 💬 **Comparte feedback** para mejoras
- 🤝 **Contribuye** siguiendo la [Guía de Contribución](CONTRIBUTING.md)

🚀 **¡Gracias por usar el Agente de CV Inteligente!**
