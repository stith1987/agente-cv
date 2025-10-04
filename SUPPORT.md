# Soporte y Ayuda

¿Necesitas ayuda con el **Agente de CV Inteligente**? ¡Estamos aquí para ayudarte! 🤝

## 🚀 Inicio Rápido

Si es tu primera vez usando el proyecto:

1. 📖 Lee el [README.md](README.md) para configuración básica
2. 📋 Revisa la [documentación de funcionalidad](FUNCIONALIDAD.md)
3. 🔧 Sigue la [guía de instalación](README.md#instalación)

## 🆘 ¿Dónde Obtener Ayuda?

### 📚 Documentación

Antes de pedir ayuda, revisa nuestra documentación:

- **[README.md](README.md)** - Configuración e instalación
- **[FUNCIONALIDAD.md](FUNCIONALIDAD.md)** - Documentación completa de características
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guía para contribuir
- **[API Docs](http://localhost:8000/docs)** - Documentación de la API (cuando esté ejecutándose)

### 🐛 Problemas Técnicos

#### Issues de GitHub

Para problemas técnicos, bugs o errores:

1. **Busca primero** en [issues existentes](https://github.com/tu-usuario/agente-cv/issues)
2. Si no encuentras tu problema, **[crea un nuevo issue](https://github.com/tu-usuario/agente-cv/issues/new)**
3. Usa las **plantillas apropiadas**:
   - 🐛 Bug Report
   - 💡 Feature Request
   - ❓ Question

#### ⚡ Problemas Comunes y Soluciones

<details>
<summary><strong>🔑 Error: OpenAI API Key no configurada</strong></summary>

```bash
ERROR: OPENAI_API_KEY no está configurada
```

**Solución**:

1. Crea un archivo `.env` en la raíz del proyecto
2. Agrega tu clave: `OPENAI_API_KEY=tu_clave_aqui`
3. Usa modelo: `OPENAI_MODEL=gpt-3.5-turbo`
4. Reinicia la aplicación con cualquier launcher

</details>

<details>
<summary><strong>🐍 Error: Entorno virtual no activado</strong></summary>

```bash
ModuleNotFoundError: No module named 'fastapi'
```

**Solución**:

```bash
# Windows
.venv\Scripts\activate

# Linux/Mac  
source .venv/bin/activate

# Verificar
pip list | findstr fastapi
```

</details>

<details>
<summary><strong>🔌 Error: Puerto en uso</strong></summary>

```bash
ERROR: Port 8000 is already in use
```

**Solución**:

```bash
# Cambiar puerto en .env
PORT=8001

# O terminar procesos
taskkill /f /im python.exe
```

</details>

<details>
<summary><strong>📊 Error: Base de datos no encontrada</strong></summary>

```bash
ERROR: ChromaDB collection not found
```

**Solución**:

```bash
# Re-indexar documentos
python -c "from rag.ingest import main; main()"

# Verificar
python -c "from rag.retriever import RAGRetriever; r=RAGRetriever(); print(f'Docs: {r.get_collection_size()}')"
```

</details>

<details>
<summary><strong>💳 Error: Quota exceeded</strong></summary>

```bash
ERROR: You exceeded your current quota
```

**Solución**:

1. Verifica tu saldo en [OpenAI Platform](https://platform.openai.com/usage)
2. Recarga créditos si es necesario
3. El sistema seguirá funcionando para consultas FAQ sin OpenAI

</details>

<details>
<summary><strong>🗄️ Error: Base de datos vacía</strong></summary>

```bash
INFO: 0 resultados encontrados
```

**Solución**:

```bash
python -m rag.ingest
```

</details>

<details>
<summary><strong>🔌 Error: Puerto ocupado</strong></summary>

```bash
ERROR: [Errno 10048] Only one usage of each socket address
```

**Solución**:

1. Cambia el puerto en `.env`: `PORT=8001`
2. O termina la aplicación existente

</details>

### 💬 Discusiones y Preguntas

Para preguntas generales, discusiones o ideas:

- **[GitHub Discussions](https://github.com/tu-usuario/agente-cv/discussions)** - Mejor para discusiones abiertas
- **[Preguntas frecuentes](#preguntas-frecuentes)** - Revisa nuestra FAQ

### 📧 Contacto Directo

Para consultas que requieren atención personal:

- **Email de soporte**: `support@ejemplo.com`
- **Tiempo de respuesta**: 24-48 horas
- **Horario**: Lunes a Viernes, 9:00 - 18:00 UTC

## ❓ Preguntas Frecuentes

### 🔧 Instalación y Configuración

<details>
<summary><strong>¿Qué versión de Python necesito?</strong></summary>

Requieres Python 3.8 o superior. Recomendamos Python 3.11+.

```bash
python --version
```

</details>

<details>
<summary><strong>¿Puedo usar el sistema sin OpenAI?</strong></summary>

Sí, parcialmente. El sistema FAQ y RAG funcionan sin OpenAI, pero no tendrás:

- Generación de respuestas contextualizadas
- Clasificación inteligente de consultas
- Evaluación automática

</details>

<details>
<summary><strong>¿Cómo agrego mis propios documentos?</strong></summary>

1. Coloca archivos `.md` en la carpeta `data/`
2. Ejecuta: `python -m rag.ingest`
3. Los documentos serán indexados automáticamente

</details>

### 🚀 Uso y Funcionalidades

<details>
<summary><strong>¿Cómo puedo acceder a la API?</strong></summary>

1. Ejecuta: `python -m api.app`
2. Ve a: `http://localhost:8000/docs`
3. Prueba el endpoint `/chat` con tu consulta

</details>

<details>
<summary><strong>¿Puedo personalizar las FAQs?</strong></summary>

Sí, puedes modificar la base de datos SQLite directamente o usar el código:

```python
from tools.faq_sql import FAQSQLTool

faq_tool = FAQSQLTool()
faq_tool.add_faq(
    question="¿Nueva pregunta?",
    answer="Nueva respuesta",
    category="categoria"
)
```

</details>

<details>
<summary><strong>¿Cómo mejoro la precisión de las respuestas?</strong></summary>

1. **Agrega más documentos** relevantes en `data/`
2. **Mejora las FAQs** con preguntas más específicas
3. **Ajusta parámetros** en `.env` como `TOP_K_RESULTS`
4. **Usa prompts más específicos** en tus consultas

</details>

### 🛠️ Desarrollo y Contribución

<details>
<summary><strong>¿Cómo puedo contribuir al proyecto?</strong></summary>

¡Excelente! Lee nuestra [Guía de Contribución](CONTRIBUTING.md) para todos los detalles.

</details>

<details>
<summary><strong>¿Cómo ejecuto los tests?</strong></summary>

```bash
# Todos los tests
python -m pytest

# Con cobertura
python -m pytest --cov=agent --cov=rag --cov=tools

# Tests específicos
python -m pytest tests/test_orchestrator.py
```

</details>

## 🔍 Debugging y Diagnóstico

### 📊 Verificar Estado del Sistema

```bash
# Verificar componentes
python -c "
from rag.retriever import SemanticRetriever
from tools.faq_sql import FAQSQLTool

# Test RAG
retriever = SemanticRetriever()
print(f'✅ RAG: {retriever.collection.count()} documentos')

# Test FAQ
faq = FAQSQLTool()
results = faq.search_faqs('test')
print(f'✅ FAQ: {len(results)} resultados disponibles')

print('🎉 Sistema funcionando correctamente')
"
```

### 📝 Logs Detallados

Para obtener más información sobre errores:

```bash
# Activar debug
export DEBUG=true  # Linux/Mac
set DEBUG=true     # Windows

# Ejecutar con logs detallados
python -m api.app
```

### 🔧 Herramientas de Diagnóstico

```bash
# Verificar dependencias
pip list

# Verificar configuración
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('OpenAI Key:', 'Configurada' if os.getenv('OPENAI_API_KEY') else 'Faltante')
print('Modelo:', os.getenv('OPENAI_MODEL', 'No configurado'))
"

# Test básico del sistema
python -c "
from agent.orchestrator import CVOrchestrator
orchestrator = CVOrchestrator()
print('✅ Orquestador inicializado correctamente')
"
```

## 📬 Plantillas de Solicitud de Ayuda

### 🐛 Para Reportar un Bug

```markdown
## 🐛 Descripción del Problema

[Describe el problema brevemente]

## 🔄 Pasos para Reproducir

1.
2.
3.

## 💻 Información del Entorno

- OS: [Windows/Mac/Linux]
- Python: [versión]
- Versión del proyecto: [si la conoces]

## 📋 Logs/Errores
```

[Pega aquí los logs relevantes]

````

## ❓ Para Hacer una Pregunta

```markdown
## ❓ Mi Pregunta
[Tu pregunta específica]

## 🎯 Lo que Estoy Tratando de Hacer
[Contexto de lo que intentas lograr]

## 🔍 Lo que He Intentado
[Pasos que ya has probado]

## 📖 Documentación Revisada
- [ ] README.md
- [ ] FUNCIONALIDAD.md
- [ ] Issues existentes
````

## 🤝 Comunidad y Recursos

### 📱 Redes Sociales

- **Twitter**: [@agente-cv](https://twitter.com/agente-cv)
- **LinkedIn**: [Agente CV Inteligente](https://linkedin.com/company/agente-cv)

### 🎓 Recursos de Aprendizaje

- **Blog**: [Artículos técnicos y tutoriales](https://blog.ejemplo.com)
- **YouTube**: [Tutoriales en video](https://youtube.com/c/agente-cv)
- **Webinars**: [Sesiones en vivo](https://ejemplo.com/webinars)

### 🌟 Hall of Fame

Reconocemos a nuestros contribuyentes más valiosos en [CONTRIBUTORS.md](CONTRIBUTORS.md).

## 📞 Información de Contacto

### Equipo de Soporte

- **Email principal**: support@ejemplo.com
- **Email técnico**: tech@ejemplo.com
- **Email de seguridad**: security@ejemplo.com

### Horarios de Soporte

- **Lunes a Viernes**: 9:00 - 18:00 UTC
- **Respuesta típica**: 24-48 horas
- **Soporte de emergencia**: Disponible para issues críticos

### Idiomas Soportados

- 🇪🇸 Español (Principal)
- 🇺🇸 English
- 🇫🇷 Français
- 🇩🇪 Deutsch

---

## 🙏 ¡Gracias por Usar Agente CV Inteligente!

Tu feedback y participación ayudan a hacer este proyecto mejor para todos. ¡No dudes en contactarnos si necesitas ayuda!

**¿Este documento te ayudó?** ⭐ Dale una estrella al repo y compártelo con otros.

**¿Falta algo?** 📝 Abre un issue o contribuye mejorando esta documentación.

---

_Última actualización: Octubre 2025_
