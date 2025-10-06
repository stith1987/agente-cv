# 📚 Índice de Documentación Git - Agente CV

> **Guía rápida**: Para encontrar cualquier documento relacionado con Git y estrategia de ramas

---

## 🚀 Para Empezar (Start Here)

### 👉 Si tienes 5 minutos:
📄 **[QUICKSTART_GIT.md](../QUICKSTART_GIT.md)**
- TL;DR completo
- Comandos esenciales
- Checklist de PR
- Comandos de emergencia

### 👉 Si tienes 20 minutos:
📄 **[GIT_WORKFLOW.md](../GIT_WORKFLOW.md)**
- Guía completa del flujo de trabajo
- Todos los comandos explicados
- Políticas y mejores prácticas
- Ejemplos paso a paso

### 👉 Acabas de llegar al proyecto:
📄 **[IMPLEMENTATION_SUMMARY.md](../IMPLEMENTATION_SUMMARY.md)**
- Resumen ejecutivo
- ¿Qué se implementó y por qué?
- Próximos pasos
- FAQ

---

## 📖 Documentación por Propósito

### 🎯 Necesito saber cómo...

#### ✨ Crear una nueva feature
1. Lee: [GIT_WORKFLOW.md](../GIT_WORKFLOW.md) → Sección "Desarrollar una Nueva Característica"
2. Ejecuta:
   ```bash
   git checkout develop
   git checkout -b feature/mi-feature
   ```
3. Usa: [Pull Request Template](../.github/pull_request_template.md)

#### 🐛 Hacer un hotfix urgente
1. Lee: [GIT_WORKFLOW.md](../GIT_WORKFLOW.md) → Sección "Hotfix de Emergencia"
2. Ejecuta:
   ```bash
   git checkout main
   git checkout -b hotfix/bug-critico
   ```
3. Sigue: El flujo rápido de hotfix

#### 📝 Actualizar documentación
1. Lee: [BRANCH_DOCUMENTATION_GUIDE.md](BRANCH_DOCUMENTATION_GUIDE.md)
2. Revisa: El checklist para tu tipo de cambio
3. Actualiza: Docs junto con el código

#### 🔍 Ver el estado de las ramas
1. Usa: [GIT_BRANCH_VISUALIZATION.md](GIT_BRANCH_VISUALIZATION.md)
2. Ejecuta:
   ```bash
   git log --all --graph --decorate --oneline
   ```
3. O instala: Git Graph extension para VSCode

#### ✅ Crear un Pull Request
1. Usa: [Pull Request Template](../.github/pull_request_template.md)
2. Revisa: [GIT_WORKFLOW.md](../GIT_WORKFLOW.md) → "Pull Request Requirements"
3. Verifica: Que los checks de CI/CD pasen

#### 🔧 Configurar mi entorno
1. Ejecuta: `scripts\setup_branches.bat` (Windows) o `./scripts/setup_branches.sh` (Linux)
2. Lee: [scripts/README.md](../scripts/README.md)
3. Configura: Protección de ramas en GitHub (ver [IMPLEMENTATION_SUMMARY.md](../IMPLEMENTATION_SUMMARY.md))

---

## 📂 Todos los Documentos

### 📋 Documentos Raíz

| Documento | Propósito | Audiencia | Tiempo de Lectura |
|-----------|-----------|-----------|-------------------|
| **[README.md](../README.md)** | Información general del proyecto | Todos | 10 min |
| **[GIT_WORKFLOW.md](../GIT_WORKFLOW.md)** | Guía completa de Git Flow | Developers | 20 min |
| **[QUICKSTART_GIT.md](../QUICKSTART_GIT.md)** | Referencia rápida | Developers | 5 min |
| **[CHANGELOG.md](../CHANGELOG.md)** | Registro de cambios | Todos | Variable |
| **[IMPLEMENTATION_SUMMARY.md](../IMPLEMENTATION_SUMMARY.md)** | Resumen de implementación | Tech Leads | 15 min |

### 📁 Documentos en /docs

| Documento | Propósito | Audiencia | Tiempo de Lectura |
|-----------|-----------|-----------|-------------------|
| **[BRANCH_DOCUMENTATION_GUIDE.md](BRANCH_DOCUMENTATION_GUIDE.md)** | Gestión de docs por rama | Developers | 15 min |
| **[GIT_BRANCH_VISUALIZATION.md](GIT_BRANCH_VISUALIZATION.md)** | Diagramas y visualizaciones | Todos | 10 min |

### ⚙️ Configuración (.github)

| Archivo | Propósito |
|---------|-----------|
| **[pull_request_template.md](../.github/pull_request_template.md)** | Template de PR |
| **[workflows/branch-protection.yml](../.github/workflows/branch-protection.yml)** | CI/CD checks |
| **[labeler.yml](../.github/labeler.yml)** | Auto-etiquetado |
| **[markdown-link-check-config.json](../.github/markdown-link-check-config.json)** | Config de validación |

### 🛠️ Scripts

| Script | Propósito | Plataforma |
|--------|-----------|------------|
| **[setup_branches.py](../scripts/setup_branches.py)** | Inicializar ramas | Todas (Python) |
| **[setup_branches.bat](../scripts/setup_branches.bat)** | Wrapper de Windows | Windows |
| **[setup_branches.sh](../scripts/setup_branches.sh)** | Wrapper de Unix | Linux/Mac |
| **[scripts/README.md](../scripts/README.md)** | Documentación de scripts | Todas |

---

## 🎓 Rutas de Aprendizaje

### 🌱 Nivel Principiante

**Objetivo**: Entender lo básico para trabajar con features

1. ✅ Leer [QUICKSTART_GIT.md](../QUICKSTART_GIT.md) (5 min)
2. ✅ Ver [GIT_BRANCH_VISUALIZATION.md](GIT_BRANCH_VISUALIZATION.md) → Diagramas (10 min)
3. ✅ Crear una feature de prueba siguiendo [GIT_WORKFLOW.md](../GIT_WORKFLOW.md) (30 min)
4. ✅ Hacer un PR usando el [Template](../.github/pull_request_template.md) (10 min)

**Total**: ~1 hora

### 🌿 Nivel Intermedio

**Objetivo**: Dominar el flujo completo y documentación

1. ✅ Todo lo de Principiante
2. ✅ Leer [GIT_WORKFLOW.md](../GIT_WORKFLOW.md) completo (20 min)
3. ✅ Leer [BRANCH_DOCUMENTATION_GUIDE.md](BRANCH_DOCUMENTATION_GUIDE.md) (15 min)
4. ✅ Practicar merge de develop → staging → main (30 min)
5. ✅ Actualizar [CHANGELOG.md](../CHANGELOG.md) con un cambio (10 min)

**Total**: ~2 horas (incluyendo nivel anterior)

### 🌳 Nivel Avanzado

**Objetivo**: Ser capaz de mantener y mejorar el sistema

1. ✅ Todo lo de Intermedio
2. ✅ Leer [IMPLEMENTATION_SUMMARY.md](../IMPLEMENTATION_SUMMARY.md) (15 min)
3. ✅ Configurar protección de ramas en GitHub (20 min)
4. ✅ Revisar y entender workflows de CI/CD (30 min)
5. ✅ Practicar un hotfix completo (30 min)
6. ✅ Crear un script personalizado siguiendo [scripts/README.md](../scripts/README.md) (1 hora)

**Total**: ~4.5 horas (incluyendo niveles anteriores)

---

## 🔍 Búsqueda Rápida

### Por Palabra Clave

| Buscas... | Ve a... |
|-----------|---------|
| "comandos git" | [QUICKSTART_GIT.md](../QUICKSTART_GIT.md) → Comandos Comunes |
| "crear feature" | [GIT_WORKFLOW.md](../GIT_WORKFLOW.md) → Flujo Normal |
| "hotfix" | [GIT_WORKFLOW.md](../GIT_WORKFLOW.md) → Hotfix de Emergencia |
| "pull request" | [pull_request_template.md](../.github/pull_request_template.md) |
| "documentación" | [BRANCH_DOCUMENTATION_GUIDE.md](BRANCH_DOCUMENTATION_GUIDE.md) |
| "visualizar ramas" | [GIT_BRANCH_VISUALIZATION.md](GIT_BRANCH_VISUALIZATION.md) |
| "changelog" | [CHANGELOG.md](../CHANGELOG.md) |
| "versiones" | [GIT_WORKFLOW.md](../GIT_WORKFLOW.md) → Versionado Semántico |
| "protección" | [IMPLEMENTATION_SUMMARY.md](../IMPLEMENTATION_SUMMARY.md) → Próximos Pasos |
| "CI/CD" | [branch-protection.yml](../.github/workflows/branch-protection.yml) |
| "scripts" | [scripts/README.md](../scripts/README.md) |
| "conflictos" | [GIT_WORKFLOW.md](../GIT_WORKFLOW.md) → Troubleshooting |

### Por Rol

#### 👨‍💻 Developer
- **Esencial**:
  - [QUICKSTART_GIT.md](../QUICKSTART_GIT.md)
  - [GIT_WORKFLOW.md](../GIT_WORKFLOW.md)
  - [Pull Request Template](../.github/pull_request_template.md)
- **Útil**:
  - [BRANCH_DOCUMENTATION_GUIDE.md](BRANCH_DOCUMENTATION_GUIDE.md)
  - [GIT_BRANCH_VISUALIZATION.md](GIT_BRANCH_VISUALIZATION.md)

#### 🧪 QA Engineer
- **Esencial**:
  - [GIT_WORKFLOW.md](../GIT_WORKFLOW.md) → Sección Staging
  - [Pull Request Template](../.github/pull_request_template.md) → Checklist
- **Útil**:
  - [CHANGELOG.md](../CHANGELOG.md)
  - [GIT_BRANCH_VISUALIZATION.md](GIT_BRANCH_VISUALIZATION.md)

#### 👔 Tech Lead
- **Esencial**:
  - [IMPLEMENTATION_SUMMARY.md](../IMPLEMENTATION_SUMMARY.md)
  - [GIT_WORKFLOW.md](../GIT_WORKFLOW.md) → Completo
  - [branch-protection.yml](../.github/workflows/branch-protection.yml)
- **Útil**:
  - Todo lo demás

#### 📝 Technical Writer
- **Esencial**:
  - [BRANCH_DOCUMENTATION_GUIDE.md](BRANCH_DOCUMENTATION_GUIDE.md)
  - [GIT_WORKFLOW.md](../GIT_WORKFLOW.md) → Gestión de Documentación
- **Útil**:
  - [QUICKSTART_GIT.md](../QUICKSTART_GIT.md)
  - [Pull Request Template](../.github/pull_request_template.md)

---

## 📊 Mapa Mental

```
                    Git Strategy
                         |
        _________________|_________________
       |                 |                 |
   Workflow         Documentation      Automation
       |                 |                 |
       |                 |                 |
  ┌────┴────┐      ┌────┴────┐      ┌────┴────┐
  |         |      |         |      |         |
Main   Branches   Docs    Templates Scripts  CI/CD
Docs                by Role           
  |         |      |         |      |         |
  |         |      |         |      |         |
GIT_     feature/  Branch   PR     setup_   branch-
WORKFLOW hotfix/   Docs     Template branches protection
         develop            
         staging            
         main
```

---

## 🎯 Casos de Uso Comunes

### Escenario 1: Nuevo Miembro del Equipo

**Usuario**: "Acabo de unirme al equipo, ¿por dónde empiezo?"

**Ruta**:
1. Leer [README.md](../README.md) → Sección Git Strategy
2. Leer [QUICKSTART_GIT.md](../QUICKSTART_GIT.md)
3. Ejecutar `scripts\setup_branches.bat` (si es necesario)
4. Crear tu primera feature de prueba

**Tiempo**: 30 min

---

### Escenario 2: Hacer mi Primera Feature

**Usuario**: "Tengo que implementar una nueva característica"

**Ruta**:
1. [GIT_WORKFLOW.md](../GIT_WORKFLOW.md) → "Desarrollar una Nueva Característica"
2. [BRANCH_DOCUMENTATION_GUIDE.md](BRANCH_DOCUMENTATION_GUIDE.md) → "Checklist: Nueva Feature"
3. [Pull Request Template](../.github/pull_request_template.md) → Llenar al terminar

**Tiempo**: 10 min lectura + desarrollo

---

### Escenario 3: Bug Crítico en Producción

**Usuario**: "¡Hay un bug en producción! ¿Qué hago?"

**Ruta**:
1. [GIT_WORKFLOW.md](../GIT_WORKFLOW.md) → "Hotfix de Emergencia"
2. [QUICKSTART_GIT.md](../QUICKSTART_GIT.md) → Comandos de Emergencia
3. Ejecutar hotfix siguiendo el flujo

**Tiempo**: 2 min lectura + fix

---

### Escenario 4: Revisar un Pull Request

**Usuario**: "Me pidieron revisar un PR"

**Ruta**:
1. [Pull Request Template](../.github/pull_request_template.md) → Checklist de Revisión
2. [GIT_WORKFLOW.md](../GIT_WORKFLOW.md) → "Políticas de Merge"
3. Verificar que pase CI/CD en [branch-protection.yml](../.github/workflows/branch-protection.yml)

**Tiempo**: 5 min guía + revisión del código

---

### Escenario 5: Actualizar Documentación

**Usuario**: "Hice cambios en el código, ¿cómo actualizo las docs?"

**Ruta**:
1. [BRANCH_DOCUMENTATION_GUIDE.md](BRANCH_DOCUMENTATION_GUIDE.md) → Tu tipo de cambio
2. Seguir el checklist específico
3. Actualizar [CHANGELOG.md](../CHANGELOG.md) si es necesario

**Tiempo**: 10 min

---

## 🔗 Enlaces Externos Útiles

- 📚 [Pro Git Book](https://git-scm.com/book/en/v2) - Libro completo de Git
- 🎮 [Learn Git Branching](https://learngitbranching.js.org/) - Tutorial interactivo
- 📖 [Git Flow Cheatsheet](https://danielkummer.github.io/git-flow-cheatsheet/) - Referencia rápida
- 📝 [Conventional Commits](https://www.conventionalcommits.org/) - Formato de commits
- 🏷️ [Semantic Versioning](https://semver.org/) - Versionado semántico
- 🐙 [GitHub Flow](https://guides.github.com/introduction/flow/) - Alternativa simplificada

---

## 🆘 Ayuda

### ¿No encuentras lo que buscas?

1. **Busca en los documentos**: Usa Ctrl+F en cada archivo
2. **Revisa el índice**: Estás aquí, busca por palabra clave
3. **Abre un issue**: [GitHub Issues](https://github.com/stith1987/agente-cv/issues)
4. **Pregunta al equipo**: En tu canal de comunicación

### Documentación Desactualizada

Si encuentras docs desactualizadas:
1. Abre un issue describiendo el problema
2. O mejor aún, crea un PR con la corrección
3. Sigue [CONTRIBUTING.md](../CONTRIBUTING.md)

---

## 📅 Mantenimiento

Este índice se actualiza:
- ✅ Cada vez que se añade un documento nuevo
- ✅ Cuando cambia la estructura
- ✅ Cuando hay feedback de usuarios

**Última actualización**: 2025-10-06
**Versión**: 1.0.0
**Mantenedor**: [@stith1987](https://github.com/stith1987)

---

## 💡 Tips Pro

1. **Marcador**: Guarda este índice como marcador para acceso rápido
2. **Búsqueda**: Usa Ctrl+F para buscar en este índice
3. **Imprime**: [QUICKSTART_GIT.md](../QUICKSTART_GIT.md) es perfecto para imprimir y tener a mano
4. **Extensiones VSCode**: 
   - Git Graph para visualizar
   - GitLens para información de commits
5. **Alias**: Configura aliases de Git para comandos frecuentes

---

**🎉 ¡Ahora sabes dónde encontrar todo! Happy Coding! 🚀**
