# Agente de CV Inteligente

Un agente de IA avanzado que utiliza RAG (Retrieval-Augmented Generation) y herramientas especializadas para responder preguntas sobre tu CV, proyectos y experiencia profesional.

## 🚀 Características

- **RAG Semántico**: Búsqueda inteligente en documentos de CV y proyectos
- **Base de FAQs**: Sistema SQL para preguntas frecuentes
- **Evaluación Automática**: LLM evaluador para auto-crítica y mejora
- **Notificaciones**: Integración con Pushover para alertas
- **API REST**: Endpoint FastAPI para integración
- **Interfaz Web**: UI con Gradio (opcional)
- **Orquestador Inteligente**: Decide automáticamente qué herramienta usar

## 📁 Estructura del Proyecto

```
├─ .env.example
├─ README.md
├─ requirements.txt
├─ data/
│  ├─ cv.md
│  ├─ proyectos/
│  │  ├─ 01-banca-digital.md
│  │  ├─ 02-arch-enterprise.md
│  └─ recortes/               # citas, publicaciones, talks
├─ rag/
│  ├─ ingest.py               # carga e indexa documentos
│  └─ retriever.py            # búsqueda semántica (top-k)
├─ tools/
│  ├─ faq_sql.py              # herramienta SQL (FAQs)
│  ├─ notify.py               # Pushover u otro canal
│  └─ tool_schemas.py         # JSON schemas para tool calling
├─ agent/
│  ├─ prompts.py              # system / evaluator / planning
│  ├─ orchestrator.py         # decide: RAG, SQL o directo
│  └─ evaluator.py            # LLM evaluador (self-critique)
├─ api/
│  ├─ app.py                  # FastAPI (endpoint /chat)
│  └─ ui_gradio.py            # Interfaz web (opcional)
└─ storage/
   ├─ vectordb/               # Chroma/FAISS index
   └─ sqlite/faq.db           # base de FAQs
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

## 🚦 Uso

### API REST

```bash
python -m api.app
```

La API estará disponible en `http://localhost:8000`

**Endpoint principal:**

```bash
POST /chat
{
  "message": "¿Cuáles son mis principales proyectos de banca digital?",
  "session_id": "user123"
}
```

### Interfaz Web

```bash
python -m api.ui_gradio
```

Accede a `http://localhost:7860` para la interfaz web.

### Uso Programático

```python
from agent.orchestrator import CVOrchestrator

orchestrator = CVOrchestrator()
response = orchestrator.process_query(
    "¿Qué experiencia tengo en arquitectura empresarial?"
)
print(response)
```

## 🔧 Configuración

### Variables de Entorno

- `OPENAI_API_KEY`: Tu clave API de OpenAI
- `OPENAI_MODEL`: Modelo a usar (default: gpt-4)
- `VECTORDB_PATH`: Ruta de la base de datos vectorial
- `SQLITE_DB_PATH`: Ruta de la base de datos SQLite
- `PUSHOVER_TOKEN`: Token de Pushover para notificaciones
- `TOP_K_RESULTS`: Número de resultados RAG (default: 5)

### Personalización

1. **Agregar documentos**: Coloca tus archivos MD en `data/`
2. **FAQs**: Edita la base SQLite en `storage/sqlite/faq.db`
3. **Prompts**: Personaliza en `agent/prompts.py`
4. **Herramientas**: Añade nuevas tools en `tools/`

## 📊 Componentes

### RAG (Retrieval-Augmented Generation)

- **Ingest**: Procesa y vectoriza documentos markdown
- **Retriever**: Búsqueda semántica con embeddings
- **Vector DB**: Almacenamiento eficiente con Chroma/FAISS

### Sistema de Herramientas

- **FAQ SQL**: Consultas estructuradas a base de FAQs
- **Notificaciones**: Alertas push via Pushover
- **Schemas**: Definiciones JSON para tool calling

### Agente Inteligente

- **Orquestador**: Routing inteligente de consultas
- **Evaluador**: Auto-crítica y mejora continua
- **Prompts**: Sistema de prompts especializados

## 🧪 Testing

```bash
# Ejecutar tests
python -m pytest tests/

# Test específico del RAG
python -m pytest tests/test_rag.py

# Test del orquestador
python -m pytest tests/test_orchestrator.py
```

## 📈 Roadmap

- [ ] Integración con más bases de datos
- [ ] Soporte para múltiples idiomas
- [ ] Dashboard de analytics
- [ ] Integración con calendarios
- [ ] Export a diferentes formatos
- [ ] Plugin para LinkedIn

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Contacto

Tu Nombre - tu.email@ejemplo.com

Enlace del Proyecto: [https://github.com/tu-usuario/agente-cv](https://github.com/tu-usuario/agente-cv)
