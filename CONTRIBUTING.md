# Guía de Contribución

¡Gracias por tu interés en contribuir al **Agente de CV Inteligente**! 🎉

Este documento te guiará a través del proceso de contribución y te ayudará a hacer contribuciones efectivas.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [¿Cómo puedo contribuir?](#cómo-puedo-contribuir)
- [Configuración del Entorno](#configuración-del-entorno)
- [Proceso de Contribución](#proceso-de-contribución)
- [Estándares de Código](#estándares-de-código)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Mejoras](#sugerir-mejoras)
- [Pull Requests](#pull-requests)

## 📜 Código de Conducta

Este proyecto y todos los participantes están regidos por nuestro [Código de Conducta](CODE_OF_CONDUCT.md). Al participar, se espera que respetes este código.

## 🤝 ¿Cómo puedo contribuir?

Hay muchas formas de contribuir al proyecto:

### 🐛 Reportar Bugs

- Usa la plantilla de bug report
- Incluye pasos para reproducir
- Proporciona información del entorno

### 💡 Sugerir Nuevas Características

- Abre un issue con la etiqueta `enhancement`
- Describe el problema que resuelve
- Propón una solución detallada

### 📖 Mejorar Documentación

- Corregir errores tipográficos
- Mejorar explicaciones
- Agregar ejemplos

### 💻 Contribuir con Código

- Corregir bugs
- Implementar nuevas características
- Optimizar rendimiento
- Agregar tests

### 🧪 Testing

- Escribir tests unitarios
- Realizar pruebas de integración
- Reportar casos edge

## 🛠️ Configuración del Entorno

### Prerrequisitos

- Python 3.8+
- Git
- Cuenta de OpenAI (para testing completo)

### Configuración Local

```bash
# 1. Fork y clonar el repositorio
git clone https://github.com/tu-usuario/agente-cv.git
cd agente-cv

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Si existe

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus claves

# 5. Inicializar base de datos
python -m rag.ingest

# 6. Ejecutar tests
python -m pytest tests/
```

### Estructura del Proyecto

```
agente-cv/
├── agent/          # Lógica del agente
├── api/            # APIs FastAPI y Gradio
├── data/           # Documentos fuente
├── rag/            # Sistema RAG
├── tools/          # Herramientas especializadas
├── storage/        # Bases de datos
├── tests/          # Tests unitarios
└── docs/           # Documentación adicional
```

## 🔄 Proceso de Contribución

### 1. Antes de Empezar

- Revisa issues existentes para evitar duplicados
- Comenta en el issue que planeas trabajar
- Espera confirmación antes de grandes cambios

### 2. Crear Branch

```bash
# Crear branch desde main
git checkout main
git pull origin main
git checkout -b feature/nombre-descriptivo

# o para bugfix
git checkout -b bugfix/descripcion-bug
```

### 3. Hacer Cambios

- Sigue los estándares de código
- Agrega tests para nuevas funcionalidades
- Actualiza documentación si es necesario
- Haz commits pequeños y descriptivos

### 4. Testing

```bash
# Ejecutar todos los tests
python -m pytest

# Con cobertura
python -m pytest --cov=agent --cov=rag --cov=tools

# Tests específicos
python -m pytest tests/test_orchestrator.py

# Linting
black . --check
flake8 .
mypy .
```

### 5. Commit y Push

```bash
# Commits descriptivos
git add .
git commit -m "feat(rag): agregar soporte para documentos PDF"

# Push al fork
git push origin feature/nombre-descriptivo
```

## 📏 Estándares de Código

### Python Code Style

- **Formatter**: Black (line length: 88)
- **Linter**: Flake8
- **Type Checking**: MyPy
- **Import Sorting**: isort

```bash
# Formatear código
black .

# Verificar style
flake8 .

# Type checking
mypy .

# Ordenar imports
isort .
```

### Convenciones de Naming

```python
# Variables y funciones: snake_case
user_query = "¿Cuáles son mis habilidades?"
def process_query(query: str) -> str:

# Clases: PascalCase
class CVOrchestrator:
class ResponseEvaluator:

# Constantes: UPPER_SNAKE_CASE
MAX_TOKENS = 1500
DEFAULT_MODEL = "gpt-3.5-turbo"

# Archivos: snake_case
orchestrator.py
faq_sql.py
```

### Documentación de Código

```python
def search_faqs(self, query: str, limit: int = 5) -> List[FAQResult]:
    """
    Buscar preguntas frecuentes por similitud.

    Args:
        query: Consulta de búsqueda
        limit: Número máximo de resultados

    Returns:
        Lista de resultados FAQ ordenados por relevancia

    Raises:
        DatabaseError: Si hay problemas con la conexión

    Example:
        >>> faq_tool = FAQSQLTool()
        >>> results = faq_tool.search_faqs("tecnologías")
        >>> print(f"Encontrados: {len(results)} resultados")
    """
```

## 🐛 Reportar Bugs

### Antes de Reportar

1. Busca en issues existentes
2. Reproduce el bug en la última versión
3. Verifica que no sea un problema de configuración

### Template de Bug Report

```markdown
## 🐛 Descripción del Bug

Descripción clara y concisa del problema.

## 🔄 Pasos para Reproducir

1. Ir a '...'
2. Hacer click en '...'
3. Scroll hasta '...'
4. Ver error

## ✅ Comportamiento Esperado

Descripción de lo que esperabas que pasara.

## 🔍 Comportamiento Actual

Descripción de lo que realmente pasó.

## 📊 Información del Entorno

- OS: [Windows 10, macOS, Ubuntu 20.04]
- Python: [3.9.0]
- Versión del proyecto: [1.0.0]
- OpenAI API: [Sí/No]

## 📎 Información Adicional

- Logs relevantes
- Screenshots si aplican
- Configuración especial
```

## 💡 Sugerir Mejoras

### Template de Feature Request

```markdown
## 🚀 Descripción de la Característica

Descripción clara de la nueva funcionalidad.

## 🎯 Problema que Resuelve

¿Qué problema específico resuelve esta característica?

## 💭 Solución Propuesta

Descripción detallada de cómo implementarías esta funcionalidad.

## 🔄 Alternativas Consideradas

Otras soluciones que consideraste.

## 📋 Criterios de Aceptación

- [ ] Criterio 1
- [ ] Criterio 2
- [ ] Criterio 3

## 🎨 Mockups/Ejemplos

Si aplican, agrega mockups o ejemplos de uso.
```

## 🔀 Pull Requests

### Antes de Crear PR

- [ ] Todos los tests pasan
- [ ] Código formateado con Black
- [ ] Sin errores de linting
- [ ] Documentación actualizada
- [ ] Tests agregados para nuevas funcionalidades
- [ ] Branch actualizado con main

### Template de Pull Request

```markdown
## 📝 Descripción

Descripción breve de los cambios realizados.

## 🔗 Issue Relacionado

Fixes #123

## 🧪 Tipo de Cambio

- [ ] Bug fix (no breaking change)
- [ ] Nueva característica (no breaking change)
- [ ] Breaking change (fix o feature que causa que funcionalidad existente no funcione)
- [ ] Documentación

## ✅ Checklist

- [ ] Mi código sigue las guías de estilo del proyecto
- [ ] He revisado mi propio código
- [ ] He comentado mi código en áreas difíciles de entender
- [ ] He hecho cambios correspondientes a la documentación
- [ ] Mis cambios no generan nuevos warnings
- [ ] He agregado tests que prueban que mi fix es efectivo o que mi feature funciona
- [ ] Tests unitarios nuevos y existentes pasan localmente

## 🧪 Tests Realizados

Describe las pruebas que realizaste.

## 📸 Screenshots

Si aplican, agrega screenshots de los cambios.
```

### Proceso de Review

1. **Automated Checks**: CI/CD ejecuta tests automáticamente
2. **Code Review**: Maintainers revisan el código
3. **Feedback**: Se proporciona feedback constructivo
4. **Iteración**: Se realizan cambios según feedback
5. **Merge**: Se integra una vez aprobado

## 🏷️ Convenciones de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>[scope opcional]: <descripción>

[cuerpo opcional]

[footer opcional]
```

### Tipos

- `feat`: Nueva característica
- `fix`: Corrección de bug
- `docs`: Solo cambios de documentación
- `style`: Cambios que no afectan el significado del código
- `refactor`: Cambios de código que no corrigen bugs ni agregan características
- `perf`: Cambios que mejoran rendimiento
- `test`: Agregar tests faltantes o corregir existentes
- `chore`: Cambios en build process o herramientas auxiliares

### Ejemplos

```bash
feat(rag): agregar soporte para documentos PDF
fix(orchestrator): corregir clasificación de consultas complejas
docs(readme): actualizar instrucciones de instalación
style(agent): formatear código con black
refactor(faq): simplificar lógica de búsqueda
perf(retriever): optimizar consultas vectoriales
test(orchestrator): agregar tests para clasificación
chore(deps): actualizar dependencias
```

## 🆘 ¿Necesitas Ayuda?

Si tienes preguntas sobre cómo contribuir:

- 💬 Abre un issue con la etiqueta `question`
- 📧 Contacta a los maintainers: `maintainers@ejemplo.com`
- 📖 Revisa la [documentación](FUNCIONALIDAD.md)
- 🤝 Únete a nuestras discusiones

## 🙏 Reconocimiento

Todos los contribuyentes serán listados en nuestro [Hall of Fame](CONTRIBUTORS.md).

---

¡Gracias por contribuir al **Agente de CV Inteligente**! 🚀
