# 🎯 Multi-LLM Plug-and-Play

Sistema unificado para invocar múltiples proveedores LLM (Large Language Models) usando una interfaz compatible con OpenAI.

## 🌟 Características

- ✅ **Interfaz única**: API compatible OpenAI para todos los proveedores
- 🔌 **Plug-and-play**: Cambia de modelo con solo cambiar la configuración
- ⚡ **Soporte asíncrono**: Generación paralela y ensembles
- 🎭 **Múltiples proveedores**: OpenAI, DeepSeek, Groq, Gemini, Ollama, etc.
- 🔀 **Sistema de Ensemble**: Compara outputs y selecciona el mejor
- 🎨 **Combinación inteligente**: Fusiona respuestas de múltiples modelos

---

## 📦 Proveedores Soportados

| Proveedor | Modelos | Base URL | Notas |
|-----------|---------|----------|-------|
| **OpenAI** | GPT-4, GPT-3.5-turbo, GPT-4o | `https://api.openai.com/v1` | Provider por defecto |
| **DeepSeek** | deepseek-chat, deepseek-coder | `https://api.deepseek.com/v1` | Alternativa económica |
| **Groq** | Mixtral-8x7b, Llama 3.x, Gemma | `https://api.groq.com/openai/v1` | Ultra rápido |
| **Ollama** | Llama, Mistral, CodeLlama | `http://localhost:11434/v1` | Local, sin API key |
| **Gemini** | gemini-pro, gemini-1.5-pro | Vía adaptador | Requiere configuración |
| **Anthropic** | Claude 3 Opus/Sonnet | Vía adaptador | Requiere configuración |

---

## 🚀 Instalación y Configuración

### 1. Variables de Entorno

Crea o actualiza tu archivo `.env`:

```env
# === OpenAI (Default) ===
OPENAI_API_KEY=sk-proj-xxxxx
OPENAI_MODEL=gpt-3.5-turbo
LLM_PROVIDER=openai

# === DeepSeek ===
# LLM_PROVIDER=deepseek
# OPENAI_API_KEY=sk-xxxxx
# OPENAI_MODEL=deepseek-chat
# OPENAI_BASE_URL=https://api.deepseek.com/v1

# === Groq ===
# LLM_PROVIDER=groq
# OPENAI_API_KEY=gsk_xxxxx
# OPENAI_MODEL=mixtral-8x7b-32768
# OPENAI_BASE_URL=https://api.groq.com/openai/v1

# === Ollama (Local) ===
# LLM_PROVIDER=ollama
# OPENAI_API_KEY=ollama
# OPENAI_MODEL=llama3.1
# OPENAI_BASE_URL=http://localhost:11434/v1
```

### 2. Para usar Ensemble (múltiples modelos)

```env
# Configura múltiples API keys
OPENAI_API_KEY=sk-xxxxx        # Para OpenAI
DEEPSEEK_API_KEY=sk-xxxxx      # Para DeepSeek
GROQ_API_KEY=gsk_xxxxx         # Para Groq
```

---

## 💻 Uso Básico

### Opción 1: Cliente Único

```python
from agent.utils.multi_llm_client import create_multi_llm_client

# Usar OpenAI
client = create_multi_llm_client(
    provider="openai",
    model="gpt-3.5-turbo"
)

# Generar respuesta
response = client.generate([
    {"role": "system", "content": "Eres un asistente útil."},
    {"role": "user", "content": "¿Qué es Python?"}
])

print(response.content)
print(f"Tokens: {response.tokens_used}")
```

### Opción 2: Cambiar de Proveedor

```python
# Usar DeepSeek en lugar de OpenAI
client = create_multi_llm_client(
    provider="deepseek",
    api_key="sk-deepseek-key",
    model="deepseek-chat"
)

response = client.generate(messages)
```

### Opción 3: Usar Groq (ultra rápido)

```python
client = create_multi_llm_client(
    provider="groq",
    api_key="gsk-your-groq-key",
    model="mixtral-8x7b-32768"
)

response = client.generate(messages)
```

---

## 🎭 Ensemble Multi-LLM

Ejecuta **múltiples modelos en paralelo** y combina sus respuestas:

```python
import asyncio
from agent.utils.multi_llm_client import MultiLLMEnsemble
from agent.utils.config import OpenAIConfig

# Configurar múltiples proveedores
configs = [
    OpenAIConfig(
        api_key="sk-openai-key",
        model="gpt-3.5-turbo",
        provider="openai"
    ),
    OpenAIConfig(
        api_key="sk-deepseek-key",
        model="deepseek-chat",
        provider="deepseek"
    ),
    OpenAIConfig(
        api_key="gsk-groq-key",
        model="mixtral-8x7b-32768",
        provider="groq"
    )
]

ensemble = MultiLLMEnsemble(configs)

async def compare_models():
    messages = [
        {"role": "system", "content": "Eres un experto en IA."},
        {"role": "user", "content": "Explica qué es un transformer"}
    ]
    
    # Generar respuestas de todos los modelos
    responses = await ensemble.generate_ensemble(messages)
    
    # Ver todas las respuestas
    for response in responses:
        print(f"{response.provider}: {response.content[:100]}...")
    
    # Seleccionar la mejor (por longitud)
    best = ensemble.select_best_response(responses, criteria="length")
    print(f"Mejor: {best.provider}")
    
    # Combinar todas en una respuesta
    combined = ensemble.combine_responses(responses)
    print(f"Combinada: {combined[:200]}...")

asyncio.run(compare_models())
```

---

## 🔧 Integración con CVOrchestrator

El orquestador ya está configurado para usar Multi-LLM automáticamente:

```python
from agent.core.orchestrator import CVOrchestrator
from agent.utils.config import AgentConfig, OpenAIConfig

# Configurar con DeepSeek
config = AgentConfig(
    openai=OpenAIConfig(
        api_key="sk-deepseek-key",
        model="deepseek-chat",
        provider="deepseek",
        base_url="https://api.deepseek.com/v1"
    )
)

orchestrator = CVOrchestrator(config)
result = orchestrator.process_query("¿Cuáles son mis proyectos?")
```

---

## 📊 Comparación de Proveedores

### Performance

| Proveedor | Velocidad | Costo | Calidad | Use Case |
|-----------|-----------|-------|---------|----------|
| **OpenAI GPT-4** | ⭐⭐⭐ | 💰💰💰 | ⭐⭐⭐⭐⭐ | Máxima calidad |
| **OpenAI GPT-3.5** | ⭐⭐⭐⭐ | 💰 | ⭐⭐⭐⭐ | Balance precio/calidad |
| **DeepSeek** | ⭐⭐⭐⭐ | 💰 | ⭐⭐⭐⭐ | Económico, muy bueno |
| **Groq Mixtral** | ⭐⭐⭐⭐⭐ | 💰 | ⭐⭐⭐⭐ | Ultra rápido |
| **Groq Llama 3.1** | ⭐⭐⭐⭐⭐ | 💰 | ⭐⭐⭐⭐ | Open source, rápido |
| **Ollama** | ⭐⭐⭐ | 🆓 | ⭐⭐⭐ | Local, privacidad |

### Precios Aproximados (por 1M tokens)

- **GPT-4**: $30 input / $60 output
- **GPT-3.5**: $0.50 input / $1.50 output
- **DeepSeek**: $0.14 input / $0.28 output
- **Groq**: Gratis (con límites)
- **Ollama**: Gratis (local)

---

## 🎯 Casos de Uso

### 1. Desarrollo: Ollama local
```env
LLM_PROVIDER=ollama
OPENAI_API_KEY=ollama
OPENAI_MODEL=llama3.1
OPENAI_BASE_URL=http://localhost:11434/v1
```

### 2. Producción económica: DeepSeek
```env
LLM_PROVIDER=deepseek
OPENAI_API_KEY=sk-deepseek-xxxxx
OPENAI_MODEL=deepseek-chat
OPENAI_BASE_URL=https://api.deepseek.com/v1
```

### 3. Máxima velocidad: Groq
```env
LLM_PROVIDER=groq
OPENAI_API_KEY=gsk-xxxxx
OPENAI_MODEL=mixtral-8x7b-32768
OPENAI_BASE_URL=https://api.groq.com/openai/v1
```

### 4. Máxima calidad: GPT-4
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-xxxxx
OPENAI_MODEL=gpt-4
```

---

## 🧪 Testing

```bash
# Probar cliente único
python examples/multi_llm_demo.py

# O específicamente
python -c "
from agent.utils.multi_llm_client import create_multi_llm_client

client = create_multi_llm_client(provider='openai')
response = client.generate([
    {'role': 'user', 'content': 'Hello!'}
])
print(response.content)
"
```

---

## 🔍 Troubleshooting

### Error: "Invalid API key"
- Verifica que la API key sea correcta para el proveedor
- DeepSeek keys empiezan con `sk-`
- Groq keys empiezan con `gsk_`

### Error: "Connection refused" (Ollama)
```bash
# Iniciar Ollama
ollama serve

# Verificar que funciona
curl http://localhost:11434/api/tags
```

### Error: "Model not found"
```bash
# Listar modelos disponibles según proveedor
# OpenAI: gpt-4, gpt-3.5-turbo, gpt-4o
# DeepSeek: deepseek-chat, deepseek-coder
# Groq: mixtral-8x7b-32768, llama-3.1-70b-versatile
# Ollama: ollama list
```

---

## 📚 Referencias

- [OpenAI API Docs](https://platform.openai.com/docs)
- [DeepSeek API](https://platform.deepseek.com/api-docs/)
- [Groq API](https://console.groq.com/docs)
- [Ollama](https://ollama.ai/library)

---

## 🎓 Próximos Pasos

1. ✅ Implementado: Cliente multi-LLM básico
2. ✅ Implementado: Sistema de ensemble
3. 🚧 En desarrollo: Adaptadores para Gemini y Claude
4. 🚧 En desarrollo: Caché de respuestas
5. 🚧 En desarrollo: Métricas y comparativas automáticas

---

**¿Preguntas?** Revisa `examples/multi_llm_demo.py` para más ejemplos.
