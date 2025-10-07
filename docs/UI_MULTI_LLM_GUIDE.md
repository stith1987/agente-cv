# 🎨 Interfaz Gradio Multi-LLM - Guía de Uso

## 🌟 Nueva Funcionalidad

Se agregó una **interfaz web mejorada** que permite:

- ✅ **Cambiar de proveedor LLM en tiempo real** (OpenAI ↔ DeepSeek ↔ Groq ↔ Ollama)
- ✅ **Selector dinámico de modelos** según proveedor
- ✅ **Ver estado de proveedores** configurados
- ✅ **Comparar respuestas** sin reiniciar la aplicación
- ✅ **Metadata visual** mostrando proveedor/modelo usado

---

## 🚀 Cómo Ejecutar

### Opción 1: Interfaz Multi-LLM (Recomendada)

```bash
# Activar entorno virtual
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Lanzar interfaz con selector de proveedores
python run_multi_llm_ui.py
```

### Opción 2: Interfaz Original

```bash
# UI tradicional (sin selector)
python run_ui_only.py
```

---

## 🎯 Uso de la Interfaz

### 1️⃣ **Seleccionar Proveedor**

En la parte superior verás:

```
⚙️ Configuración de Proveedor LLM
┌─────────────┬──────────────────┬──────────┐
│  Proveedor  │      Modelo      │  Aplicar │
└─────────────┴──────────────────┴──────────┘
```

**Pasos:**

1. Selecciona un proveedor en el dropdown (ej: "DeepSeek")
2. El dropdown de modelos se actualiza automáticamente
3. Selecciona un modelo (ej: "deepseek-chat")
4. Haz clic en "🔄 Aplicar"
5. Verás confirmación: `✅ Proveedor cambiado a 🧠 DeepSeek`

### 2️⃣ **Hacer Preguntas**

```
💬 Chat
┌──────────────────────────────────────┐
│ Conversación                         │
│                                      │
│ Usuario: ¿Cuáles son mis proyectos? │
│ Agente: [Respuesta...]              │
└──────────────────────────────────────┘

Escribe tu pregunta aquí...
[📤 Enviar] [🗑️ Limpiar]
☑ Evaluar respuesta
```

### 3️⃣ **Ver Información de Respuesta**

En el panel derecho verás:

```
📊 Información
────────────────────────────
Proveedor: 🧠 DeepSeek
Modelo: deepseek-chat
Fuentes: rag, faq
Tiempo: 1.23s
Contexto: 456 chars
Evaluación: 8.5/10
```

### 4️⃣ **Comparar Proveedores**

**Ejemplo: Comparar OpenAI vs DeepSeek**

1. **Con OpenAI:**

   - Selecciona "OpenAI" → "gpt-3.5-turbo"
   - Pregunta: "¿Qué tecnologías domino?"
   - Observa: Tiempo de respuesta, calidad

2. **Cambiar a DeepSeek:**

   - Selecciona "DeepSeek" → "deepseek-chat"
   - Haz clic en "🔄 Aplicar"
   - Pregunta lo mismo
   - Compara: Velocidad, costo, calidad

3. **Probar con Groq:**
   - Selecciona "Groq" → "mixtral-8x7b-32768"
   - Aplica
   - Misma pregunta
   - Nota: ⚡ Ultra rápido

---

## 📊 Estado de Proveedores

Haz clic en **"Ver Estado de Proveedores"** para ver:

```
📊 Estado de Proveedores

✅ 🤖 OpenAI - 4 modelos disponibles
✅ 🧠 DeepSeek - 2 modelos disponibles
❌ ⚡ Groq - Requiere GROQ_API_KEY en .env
✅ 🦙 Ollama - 4 modelos disponibles
```

---

## ⚙️ Configuración

### Variables de Entorno Necesarias

Para que todos los proveedores estén disponibles:

```env
# OpenAI (siempre funciona con OPENAI_API_KEY)
OPENAI_API_KEY=sk-proj-xxxxx

# DeepSeek (opcional)
DEEPSEEK_API_KEY=sk-xxxxx

# Groq (opcional)
GROQ_API_KEY=gsk-xxxxx

# Ollama no requiere API key, solo que esté corriendo
```

### Probar con un Solo Proveedor

Si solo tienes OpenAI configurado:

1. La UI mostrará solo OpenAI disponible ✅
2. DeepSeek, Groq aparecerán como ❌
3. Puedes usar OpenAI normalmente
4. Cuando configures otros, estarán disponibles automáticamente

---

## 🎬 Ejemplos de Casos de Uso

### Caso 1: Desarrollo (sin costo)

```
1. Seleccionar: Ollama → llama3.1
2. Desarrollar y probar localmente
3. Sin gastar en API calls
```

### Caso 2: Producción económica

```
1. Seleccionar: DeepSeek → deepseek-chat
2. 99% más barato que GPT-4
3. Calidad muy buena
```

### Caso 3: Máxima velocidad

```
1. Seleccionar: Groq → mixtral-8x7b-32768
2. Respuestas en <1 segundo
3. Gratis (con límites)
```

### Caso 4: Máxima calidad

```
1. Seleccionar: OpenAI → gpt-4
2. Mejor calidad de respuestas
3. Mayor costo
```

---

## 💡 Tips

### Tip 1: Comparación A/B

```
1. Pregunta con GPT-4
2. Guarda la respuesta
3. Cambia a DeepSeek
4. Misma pregunta
5. Compara calidad/costo
```

### Tip 2: Fallback automático

```
1. Si un proveedor falla
2. Cambiar rápidamente a otro
3. Sin reiniciar la aplicación
```

### Tip 3: Testing de modelos

```
1. Probar pregunta compleja
2. Con cada proveedor
3. Documentar resultados
4. Elegir el óptimo por uso
```

---

## 🐛 Troubleshooting

### Problema: "❌ Proveedor no configurado"

**Solución:**

```bash
# Ver qué falta
python quickstart_multi_llm.py

# Añadir API key en .env
DEEPSEEK_API_KEY=sk-xxxxx

# Reiniciar UI (o refrescar página)
```

### Problema: Ollama no disponible

**Solución:**

```bash
# Iniciar Ollama
ollama serve

# Verificar
curl http://localhost:11434/api/tags

# Descargar modelo si es necesario
ollama pull llama3.1
```

### Problema: Cambio no se aplica

**Solución:**

1. Verifica que hiciste clic en "🔄 Aplicar"
2. Mira el mensaje de estado
3. Si hay error, revisa los logs en la terminal

---

## 📈 Beneficios de la UI

| Funcionalidad             | Beneficio                       |
| ------------------------- | ------------------------------- |
| **Cambio en tiempo real** | No reiniciar aplicación         |
| **Comparación A/B**       | Elegir mejor proveedor por caso |
| **Estado visual**         | Ver qué está configurado        |
| **Metadata detallada**    | Debugging y optimización        |
| **Evaluación opcional**   | Métricas de calidad             |

---

## 🎯 Próximos Pasos

1. **Prueba la interfaz:**

   ```bash
   python run_multi_llm_ui.py
   ```

2. **Configura más proveedores:**

   - Añade GROQ_API_KEY para ultra velocidad
   - Añade DEEPSEEK_API_KEY para bajo costo

3. **Compara resultados:**

   - Misma pregunta, diferentes proveedores
   - Documenta cuál funciona mejor para tu caso

4. **Optimiza costos:**
   - Usa DeepSeek/Groq para preguntas simples
   - Reserva GPT-4 para preguntas complejas

---

## 📚 Recursos Adicionales

- **Guía completa**: `docs/MULTI_LLM_GUIDE.md`
- **Demo CLI**: `examples/multi_llm_demo.py`
- **Quickstart**: `quickstart_multi_llm.py`
- **Resumen técnico**: `IMPLEMENTATION_MULTI_LLM.md`

---

**🎉 ¡Disfruta la flexibilidad de Multi-LLM!**
