# Agent Module - Refactored Architecture

## 🏗️ Nueva Estructura

El módulo `agent` ha sido completamente refactorizado para mejorar la mantenibilidad, identificabilidad y funcionalidad. La nueva estructura separa responsabilidades y proporciona mejor organización del código.

```
agent/
├── __init__.py                 # Punto de entrada principal
├── core/                       # Componentes centrales
│   ├── __init__.py
│   ├── orchestrator.py         # Orquestador principal refactorizado
│   ├── query_classifier.py     # Clasificador de consultas inteligente
│   └── response_evaluator.py   # Evaluador de respuestas avanzado
├── specialists/                # Agentes especializados
│   ├── __init__.py
│   ├── clarifier.py           # Agente de aclaración mejorado
│   └── email_handler.py       # Agente de email refactorizado
└── utils/                      # Utilidades y configuración
    ├── __init__.py
    ├── config.py              # Configuración centralizada
    ├── logger.py              # Sistema de logging avanzado
    └── prompts.py             # Gestor de prompts centralizado
```

## 🚀 Características Principales

### ✅ Mejoras de Mantenibilidad

- **Separación clara de responsabilidades** por módulos especializados
- **Configuración centralizada** mediante `AgentConfig`
- **Logging avanzado** con niveles y archivos configurables
- **Gestión de prompts centralizada** con `PromptManager`
- **Arquitectura modular** que facilita testing y extensiones

### 🔍 Mejoras de Identificabilidad

- **Nombres de clases claros** y específicos por funcionalidad
- **Documentación completa** en todos los módulos
- **Tipado estático** con type hints en todas las funciones
- **Enums** para categorías y constantes bien definidas
- **Estructura de directorios intuitiva**

### ⚡ Mejoras de Funcionalidad

- **Clasificación inteligente** de consultas con reglas de negocio
- **Evaluación avanzada** de respuestas with métricas detalladas
- **Manejo de errores robusto** con fallbacks automáticos
- **Estadísticas detalladas** para monitoreo y análisis
- **Sistema de configuración flexible** desde variables de entorno

## 📋 Migración desde Estructura Anterior

### Importaciones Actualizadas

**Antes:**

```python
from agent.orchestrator import CVOrchestrator
from agent.clarifier import ClarifierAgent
from agent.email_agent import EmailAgent
from agent.evaluator import ResponseEvaluator
```

**Ahora:**

```python
from agent.core.orchestrator import CVOrchestrator
from agent.specialists.clarifier import ClarifierAgent
from agent.specialists.email_handler import EmailAgent
from agent.core.response_evaluator import ResponseEvaluator
```

**O usando el punto de entrada principal:**

```python
from agent import CVOrchestrator, ClarifierAgent, EmailAgent, ResponseEvaluator
```

### Inicialización Actualizada

**Antes:**

```python
orchestrator = CVOrchestrator()
```

**Ahora:**

```python
from agent.utils.config import AgentConfig

config = AgentConfig.from_env()  # Carga desde variables de entorno
orchestrator = CVOrchestrator(config)
```

## 🔧 Configuración

### Variables de Entorno Requeridas

```bash
# OpenAI
OPENAI_API_KEY=tu_api_key
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7

# Email (opcional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=tu_email@gmail.com
SMTP_PASSWORD=tu_password
FROM_EMAIL=tu_email@gmail.com

# Configuraciones adicionales
RAG_SIMILARITY_THRESHOLD=0.7
RAG_TOP_K=5
FAQ_LIMIT=10
LOG_LEVEL=INFO
```

### Configuración Programática

```python
from agent.utils.config import AgentConfig, OpenAIConfig, EmailConfig

# Configuración personalizada
config = AgentConfig(
    openai=OpenAIConfig(
        api_key="tu_api_key",
        model="gpt-4",
        temperature=0.7
    ),
    email=EmailConfig(
        smtp_server="smtp.gmail.com",
        username="tu_email@gmail.com",
        password="tu_password"
    ),
    rag_similarity_threshold=0.8,
    log_level="DEBUG"
)

orchestrator = CVOrchestrator(config)
```

## 📊 Uso Avanzado

### Clasificación de Consultas

```python
from agent.core.query_classifier import QueryClassifier
from agent.utils.config import AgentConfig

classifier = QueryClassifier(AgentConfig.from_env())
classification = classifier.classify("¿Qué experiencia tienes en microservicios?")

print(f"Categoría: {classification.category}")
print(f"Tool recomendado: {classification.recommended_tool}")
print(f"Confianza: {classification.confidence}%")
```

### Evaluación de Respuestas

```python
from agent.core.response_evaluator import ResponseEvaluator

evaluator = ResponseEvaluator(AgentConfig.from_env())
evaluation = evaluator.evaluate_response(
    query="¿Qué proyectos has desarrollado?",
    response="He desarrollado varios proyectos en fintech...",
    context="Información del CV..."
)

print(f"Puntuación general: {evaluation.scores.overall_score:.1f}/10")
print(f"Fortalezas: {evaluation.strengths}")
print(f"Sugerencias: {evaluation.suggestions}")
```

### Logging Avanzado

```python
from agent.utils.logger import AgentLogger

logger = AgentLogger("mi_componente", level="DEBUG", log_to_file=True)

logger.info("Procesando consulta")
logger.log_query("consulta ejemplo", "RAG", 1.5, True)
logger.log_tool_usage("rag_search", {"query": "test"}, True, 0.8)
```

## 🧪 Testing

```python
# Ejemplo de test unitario
import unittest
from agent.core.query_classifier import QueryClassifier, QueryCategory
from agent.utils.config import AgentConfig

class TestQueryClassifier(unittest.TestCase):
    def setUp(self):
        self.config = AgentConfig.from_env()
        self.classifier = QueryClassifier(self.config)

    def test_basic_query_classification(self):
        classification = self.classifier.classify("¿Cuál es tu email?")
        self.assertEqual(classification.category, QueryCategory.BASIC)

    def test_technical_query_classification(self):
        classification = self.classifier.classify("¿Qué experiencia tienes en microservicios?")
        self.assertEqual(classification.category, QueryCategory.TECHNICAL)
```

## 📈 Monitoreo y Estadísticas

```python
# Obtener estadísticas del orquestador
stats = orchestrator.get_session_stats()
print(f"Consultas procesadas: {stats['total_queries']}")
print(f"Tasa de éxito: {stats['classifier_stats']['success_rate']}%")

# Obtener estadísticas específicas
classifier_stats = orchestrator.query_classifier.get_stats()
evaluator_stats = orchestrator.response_evaluator.get_stats()
email_stats = orchestrator.email_agent.get_stats()
```

## 🔄 Compatibilidad

Durante la transición, se mantiene compatibilidad con las importaciones antiguas, pero se recomienda migrar a la nueva estructura para aprovechar todas las mejoras.

## 🛠️ Extensibilidad

La nueva arquitectura facilita la adición de nuevos componentes:

1. **Nuevos agentes especializados** en `agent/specialists/`
2. **Nuevos evaluadores** en `agent/core/`
3. **Nuevas utilidades** en `agent/utils/`
4. **Nuevos tipos de prompts** en `PromptManager`

## 📝 Notas de Migración

- Los archivos antiguos se mantienen como backup con extensión `.backup`
- Se incluye capa de compatibilidad temporal
- Logging mejorado ayuda a identificar problemas durante la migración
- Todas las configuraciones ahora son centralizadas y validadas

---

**¡La refactorización está completa y lista para uso!** 🎉
