# 🚀 Inicio Rápido - Estrategia de Ramas Git

## 📋 TL;DR

```bash
# 1. Configurar ramas (solo una vez)
scripts\setup_branches.bat

# 2. Crear una feature
git checkout develop
git checkout -b feature/mi-feature

# 3. Trabajar y commitear
git add .
git commit -m "feat: mi nueva característica"

# 4. Push y crear PR
git push -u origin feature/mi-feature
# Crear PR en GitHub hacia develop

# 5. Después del merge, limpiar
git checkout develop
git pull origin develop
git branch -d feature/mi-feature
```

## 🌳 Ramas Principales

| Rama        | Propósito              | Deploy a       |
| ----------- | ---------------------- | -------------- |
| `main`      | Producción estable     | 🚀 Production  |
| `staging`   | Pre-producción/QA      | 🧪 Staging     |
| `develop`   | Desarrollo activo      | 🔧 Development |
| `feature/*` | Nueva característica   | -              |
| `hotfix/*`  | Fix urgente producción | -              |

## 🔄 Flujo de Trabajo

```
feature/xxx → develop → staging → main
                  ↑                  ↓
                  └─── hotfix/xxx ──┘
```

## 📝 Convenciones de Commit

```
feat:     Nueva característica
fix:      Corrección de bug
docs:     Cambios en documentación
style:    Formateo de código
refactor: Refactorización
test:     Añadir/modificar tests
chore:    Tareas de mantenimiento
```

## ✅ Checklist PR

- [ ] Tests pasan
- [ ] Documentación actualizada
- [ ] CHANGELOG.md actualizado (si es necesario)
- [ ] Sin conflictos con rama base
- [ ] Código revisado

## 🔗 Documentación Completa

- 📖 [GIT_WORKFLOW.md](GIT_WORKFLOW.md) - Guía completa
- 📚 [BRANCH_DOCUMENTATION_GUIDE.md](docs/BRANCH_DOCUMENTATION_GUIDE.md) - Docs por rama
- 📝 [Pull Request Template](.github/pull_request_template.md) - Template de PR

## 🆘 Comandos de Emergencia

```bash
# Deshacer último commit (mantener cambios)
git reset --soft HEAD~1

# Actualizar feature con cambios de develop
git checkout feature/mi-feature
git rebase develop

# Revertir un merge en main
git revert -m 1 <commit-hash>

# Ver diferencias entre ramas
git diff develop..staging

# Limpiar ramas ya mergeadas
git branch --merged develop | grep -v "develop" | xargs git branch -d
```

## 💡 Tips

1. **Siempre** actualiza develop antes de crear una feature
2. **Nunca** hagas push directo a main/staging
3. **Siempre** crea un PR para review
4. Mantén las features **pequeñas** (< 500 líneas)
5. Actualiza **docs con el código**

## 🎯 Versiones

Seguimos [Semantic Versioning](https://semver.org/):

```
v MAJOR.MINOR.PATCH
  1.2.3

MAJOR: Breaking changes
MINOR: Nuevas features compatibles
PATCH: Bug fixes
```

## 📞 Ayuda

- 🐛 Problemas: [Abrir Issue](https://github.com/stith1987/agente-cv/issues)
- 💬 Preguntas: Ver [GIT_WORKFLOW.md](GIT_WORKFLOW.md)
- 🤝 Contribuir: Ver [CONTRIBUTING.md](CONTRIBUTING.md)
