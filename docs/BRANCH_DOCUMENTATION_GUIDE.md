# Guía de Documentación por Ramas

## 📚 Filosofía de Documentación

> "La documentación desactualizada es peor que no tener documentación"

En este proyecto, la documentación **SIEMPRE** debe estar sincronizada con el código. Cada rama tiene su propósito y su nivel de documentación correspondiente.

---

## 🌳 Documentación por Rama

### 1. Rama `main` (Producción)

#### 🎯 Propósito
Documentación oficial y estable que refleja exactamente lo que está en producción.

#### 📄 Archivos Obligatorios

```
agente-cv/
├── README.md                          # ⭐ Información principal
├── CHANGELOG.md                       # 📝 Historial de versiones
├── LICENSE                            # 📜 Licencia del proyecto
├── CODE_OF_CONDUCT.md                 # 🤝 Código de conducta
├── CONTRIBUTING.md                    # 👥 Guía de contribución
├── SECURITY.md                        # 🔒 Política de seguridad
├── SUPPORT.md                         # 💬 Información de soporte
├── GIT_WORKFLOW.md                    # 🔄 Estrategia de ramas
│
├── docs/
│   ├── README.md                      # Índice de documentación
│   ├── INSTALLATION.md                # Guía de instalación
│   ├── DEPLOYMENT.md                  # Guía de despliegue
│   ├── API_REFERENCE.md               # Referencia de API
│   ├── USER_GUIDE.md                  # Manual de usuario
│   ├── FAQ.md                         # Preguntas frecuentes
│   ├── TROUBLESHOOTING.md             # Solución de problemas
│   └── ARCHITECTURE.md                # Documentación arquitectónica
│
├── ARQUITECTURA_SOFTWARE.md           # Arquitectura de software
├── ARQUITECTURA_DATOS.md              # Arquitectura de datos
├── ARQUITECTURA_PROMPTS.md            # Arquitectura de prompts
├── ARQUITECTURA_SOLUCION.md           # Arquitectura de solución
│
├── README_DOCKER.md                   # Documentación Docker
├── DOCKER_*.md                        # Guías Docker específicas
│
└── examples/
    └── README.md                      # Documentación de ejemplos
```

#### ✅ Requisitos
- **Versión documentada**: Debe coincidir con el tag de release
- **Sin WIP**: No debe haber menciones a "trabajo en progreso"
- **Links validados**: Todos los enlaces internos deben funcionar
- **Ejemplos probados**: Todos los ejemplos de código deben funcionar
- **Screenshots actualizados**: Las imágenes deben reflejar la UI actual

#### 🔄 Actualización
- Se actualiza **SOLO** cuando se hace merge desde `staging`
- Cada merge debe incluir actualización de CHANGELOG.md
- Se crea un tag de versión después de cada merge

---

### 2. Rama `staging` (QA/Pre-producción)

#### 🎯 Propósito
Documentación lista para producción, en fase de validación final.

#### 📄 Archivos
Mismos que `main`, más:

```
docs/
├── QA_CHECKLIST.md                    # Checklist de QA
├── TESTING_GUIDE.md                   # Guía de pruebas
└── RELEASE_NOTES_DRAFT.md             # Borrador de release notes
```

#### ✅ Requisitos
- **Candidato a producción**: Debe estar completa y revisada
- **QA Sign-off**: Debe pasar revisión de QA
- **No breaking changes sin documentar**: Cualquier cambio mayor debe estar documentado
- **Migración documentada**: Si hay cambios de esquema, deben estar documentados

#### 🔄 Actualización
- Se actualiza cuando se hace merge desde `develop`
- QA revisa y valida la documentación
- Se pueden hacer ajustes menores antes de merge a `main`

---

### 3. Rama `develop` (Desarrollo)

#### 🎯 Propósito
Documentación activa que puede incluir features en desarrollo.

#### 📄 Archivos
Todos los anteriores, más:

```
docs/
├── ROADMAP.md                         # 🗺️ Roadmap de desarrollo
├── WIP_FEATURES.md                    # 🚧 Features en progreso
├── TECHNICAL_DECISIONS.md             # 💡 Decisiones técnicas
├── DEVELOPMENT_NOTES.md               # 📓 Notas de desarrollo
├── EXPERIMENTAL.md                    # 🧪 Features experimentales
└── TODO.md                            # ✔️ Lista de tareas pendientes
```

#### ✅ Requisitos
- **Puede ser incompleta**: Está bien tener TODOs
- **Marca WIP**: Indica claramente qué está en progreso
- **Actualización frecuente**: Se actualiza con cada feature completada
- **Enlaces a PRs**: Puede referenciar PRs abiertos

#### 🔄 Actualización
- Se actualiza con cada merge de feature branch
- Los developers actualizan al completar features
- Se limpia antes de merge a `staging`

---

### 4. Ramas `feature/*` (Características)

#### 🎯 Propósito
Documentación específica de la feature en desarrollo.

#### 📄 Archivos
Pueden incluir:

```
docs/
└── features/
    └── nombre-feature/
        ├── SPEC.md                    # Especificación
        ├── IMPLEMENTATION.md          # Detalles de implementación
        ├── TESTING.md                 # Plan de pruebas
        └── EXAMPLES.md                # Ejemplos de uso
```

#### ✅ Requisitos
- **Enfocada**: Solo documenta la feature específica
- **Temporal**: Se mergea o elimina
- **Actualiza docs principales**: Al completar, actualizar README, etc.

#### 🔄 Actualización
- Se crea al inicio de la feature
- Se actualiza durante el desarrollo
- Se integra a `develop` al completar

---

### 5. Ramas `hotfix/*` (Correcciones)

#### 🎯 Propósito
Documentación de correcciones urgentes.

#### 📄 Archivos
Actualizar:

```
CHANGELOG.md                           # Añadir entrada de hotfix
docs/TROUBLESHOOTING.md                # Si el bug era común
README.md                              # Si afecta instalación/uso
```

#### ✅ Requisitos
- **Mínima pero precisa**: Documenta el fix sin excesos
- **Update CHANGELOG**: Siempre actualizar el changelog
- **Sync a develop**: Debe mergearse también a develop

---

## 📋 Checklist de Documentación por Tipo de Cambio

### ✨ Nueva Feature

```markdown
- [ ] Actualizar README.md (sección de features)
- [ ] Añadir ejemplos en examples/
- [ ] Actualizar API_REFERENCE.md si hay nuevos endpoints
- [ ] Añadir tests documentados
- [ ] Actualizar CHANGELOG.md
- [ ] Crear docs/features/ si es compleja
- [ ] Actualizar ROADMAP.md (marcar como completada)
- [ ] Screenshots/GIFs si hay UI nueva
```

### 🐛 Bug Fix

```markdown
- [ ] Actualizar CHANGELOG.md
- [ ] Añadir a TROUBLESHOOTING.md si era común
- [ ] Actualizar FAQ.md si generaba preguntas
- [ ] Documentar el fix en el commit message
```

### 📚 Cambio Solo de Documentación

```markdown
- [ ] Verificar que no hay typos
- [ ] Validar todos los enlaces
- [ ] Probar ejemplos de código
- [ ] Actualizar fecha de última modificación
- [ ] Incrementar versión del doc si es mayor
```

### 🏗️ Refactor

```markdown
- [ ] Actualizar diagramas de arquitectura
- [ ] Actualizar ARCHITECTURE.md
- [ ] Documentar razones en TECHNICAL_DECISIONS.md
- [ ] Actualizar comentarios en código
- [ ] Actualizar guías de desarrollo
```

### 💥 Breaking Change

```markdown
- [ ] ⚠️ CHANGELOG.md con warning prominente
- [ ] Documentar migración paso a paso
- [ ] Actualizar ejemplos antiguos
- [ ] Crear guía de migración específica
- [ ] Actualizar versión MAJOR
- [ ] Avisar en README.md
- [ ] Deprecation notices si aplica
```

---

## 🔧 Herramientas y Scripts

### Script de Validación de Docs

Crea: `scripts/validate_docs.py`

```python
#!/usr/bin/env python3
"""
Valida que la documentación esté sincronizada
"""
import os
import re
from pathlib import Path

def check_required_files(branch):
    """Verifica archivos obligatorios por rama"""
    required = {
        'main': [
            'README.md', 'CHANGELOG.md', 'LICENSE',
            'CONTRIBUTING.md', 'SECURITY.md'
        ],
        'staging': [
            'docs/QA_CHECKLIST.md', 'docs/TESTING_GUIDE.md'
        ],
        'develop': [
            'docs/ROADMAP.md', 'docs/WIP_FEATURES.md'
        ]
    }
    
    # Implementar lógica de validación
    pass

def check_broken_links():
    """Verifica enlaces rotos en Markdown"""
    pass

def check_code_examples():
    """Verifica que ejemplos de código funcionen"""
    pass

if __name__ == '__main__':
    # Ejecutar validaciones
    pass
```

### Pre-commit Hook

Crea: `.git/hooks/pre-commit`

```bash
#!/bin/bash
# Valida documentación antes de commit

echo "🔍 Validando documentación..."

# Verificar que CHANGELOG esté actualizado
if git diff --cached --name-only | grep -qE "agent/|api/|rag/"; then
    if ! git diff --cached --name-only | grep -q "CHANGELOG.md"; then
        echo "⚠️  Cambios en código pero no en CHANGELOG.md"
        echo "   Por favor actualiza el CHANGELOG"
        exit 1
    fi
fi

# Verificar links en archivos .md modificados
for file in $(git diff --cached --name-only | grep ".md$"); do
    echo "Verificando enlaces en $file..."
    # Implementar verificación de enlaces
done

echo "✅ Validación de documentación completa"
```

---

## 📐 Plantillas de Documentación

### Template: Nueva Feature

```markdown
# Feature: [Nombre]

## 📋 Descripción
[Descripción concisa de la feature]

## 🎯 Objetivos
- Objetivo 1
- Objetivo 2

## 💡 Motivación
[Por qué se implementó esta feature]

## 🚀 Uso

### Instalación
\```bash
# Comandos de instalación
\```

### Ejemplo Básico
\```python
# Código de ejemplo
\```

### Ejemplo Avanzado
\```python
# Código avanzado
\```

## ⚙️ Configuración

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| param1    | str  | "default" | Descripción |

## 🔗 API Reference

### Función principal
\```python
def feature_function(param1: str, param2: int) -> Result:
    """
    Descripción de la función
    
    Args:
        param1: Descripción
        param2: Descripción
    
    Returns:
        Result: Descripción del resultado
        
    Raises:
        ValueError: Cuando...
    """
\```

## 🧪 Testing

### Tests Incluidos
- Test 1: Descripción
- Test 2: Descripción

### Ejecutar Tests
\```bash
pytest tests/test_feature.py
\```

## ⚠️ Limitaciones Conocidas
- Limitación 1
- Limitación 2

## 🔮 Futuras Mejoras
- [ ] Mejora 1
- [ ] Mejora 2

## 📚 Referencias
- [Link 1](url)
- [Link 2](url)

---
**Autor**: @username
**Fecha**: YYYY-MM-DD
**Versión**: v1.0.0
```

---

## 🔄 Workflow de Documentación

### Diagrama de Flujo

```
[Feature Branch]
    │
    ├─> Crear docs/features/
    ├─> Documentar durante desarrollo
    ├─> Actualizar ejemplos
    │
    ↓ PR Review
    │
[Develop]
    │
    ├─> Integrar docs de feature
    ├─> Actualizar README
    ├─> Actualizar ROADMAP
    │
    ↓ Ready for QA
    │
[Staging]
    │
    ├─> Validar documentación
    ├─> Crear release notes draft
    ├─> QA review de docs
    │
    ↓ QA Approved
    │
[Main]
    │
    ├─> Finalizar CHANGELOG
    ├─> Publicar release notes
    ├─> Tag de versión
    └─> 🎉 Documentation Released!
```

---

## 🎨 Mejores Prácticas

### ✅ DO (Hacer)

1. **Actualizar docs con el código**: En el mismo commit o PR
2. **Usar ejemplos funcionales**: Código que realmente funcione
3. **Incluir screenshots**: Una imagen vale más que mil palabras
4. **Versionar la documentación**: Indicar para qué versión es válida
5. **Links relativos**: Usar paths relativos para links internos
6. **Índices claros**: Tabla de contenidos en docs largas
7. **Formato consistente**: Seguir el estilo del proyecto
8. **Actualizar CHANGELOG**: Con cada cambio significativo

### ❌ DON'T (No Hacer)

1. **No dejar TODOs en main**: Limpialo antes de mergear
2. **No copiar docs desactualizadas**: Mejor actualizarlas
3. **No hardcodear URLs**: Usar variables o config
4. **No duplicar información**: Usar referencias
5. **No asumir conocimiento**: Explicar conceptos
6. **No ignorar typos**: Revisar ortografía
7. **No omitir prerequisitos**: Listar dependencias
8. **No documentar código obvio**: Enfócate en lo complejo

---

## 📊 Métricas de Documentación

### Indicadores de Calidad

- ✅ **Cobertura**: % de funciones documentadas
- ✅ **Actualización**: Tiempo desde último cambio de código
- ✅ **Ejemplos**: Número de ejemplos funcionales
- ✅ **Links**: % de links funcionales
- ✅ **Feedback**: Issues relacionadas con docs

### Herramienta de Métricas

```bash
# Contar funciones documentadas
find . -name "*.py" -exec grep -l "\"\"\"" {} \; | wc -l

# Verificar antiguedad de docs
ls -lt docs/*.md | head -10

# Contar ejemplos
find examples/ -name "*.py" | wc -l
```

---

## 🆘 FAQs de Documentación

### P: ¿Cuándo actualizar la documentación?
**R**: Siempre con el código, en el mismo PR.

### P: ¿Qué pasa si olvido actualizar docs?
**R**: El revisor rechazará el PR. Es un requisito.

### P: ¿Dónde documento features experimentales?
**R**: En `develop`, en `docs/EXPERIMENTAL.md`

### P: ¿Cómo documento breaking changes?
**R**: CHANGELOG con warning, guía de migración, y update en README.

### P: ¿Necesito documentar cada función?
**R**: Funciones públicas sí, privadas opcionalmente.

### P: ¿Puedo usar español en docs internas?
**R**: Sí, pero README y docs públicas en inglés es recomendado.

---

## 📞 Contacto

¿Dudas sobre documentación? Abre un issue con el label `documentation`.

---

**Última actualización**: 2025-10-06
**Mantenido por**: Tech Lead Team
