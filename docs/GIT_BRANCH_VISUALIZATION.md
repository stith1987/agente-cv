# 🌳 Visualización de la Estrategia de Ramas

## 🎨 Diagrama de Flujo Principal

```
                    PRODUCCIÓN
                        ⬇️
    ┌────────────────────────────────────────┐
    │              main (v1.0.0)             │ ← 🚀 Deploy a Producción
    └────────────────┬───────────────────────┘
                     │
                     │ PR (QA Approved)
                     ↑
    ┌────────────────────────────────────────┐
    │             staging                     │ ← 🧪 Deploy a Staging/QA
    └────────────────┬───────────────────────┘
                     │
                     │ PR (Tests Pass)
                     ↑
    ┌────────────────────────────────────────┐
    │             develop                     │ ← 🔧 Deploy a Dev
    └────┬───────────┬───────────┬───────────┘
         ↑           ↑           ↑
         │           │           │
    ┌────┴────┐ ┌───┴────┐ ┌────┴─────┐
    │feature/ │ │feature/│ │ feature/ │
    │  auth   │ │  api   │ │   rag    │
    └─────────┘ └────────┘ └──────────┘
```

## 🔄 Ciclo de Vida de una Feature

```
Día 1-3: Desarrollo
┌─────────────────┐
│   1. Crear      │
│   feature/xxx   │ ← git checkout -b feature/xxx
│   desde develop │
└────────┬────────┘
         │
         │ Coding...
         ↓
┌─────────────────┐
│   2. Commits    │ ← git commit -m "feat: ..."
│   frecuentes    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   3. Push y     │ ← git push origin feature/xxx
│   crear PR      │
└────────┬────────┘

Día 3-4: Review
         │
         │ Code Review
         ↓
┌─────────────────┐
│   4. Merge a    │ ← Después de aprobación
│   develop       │
└────────┬────────┘

Día 5-7: QA
         │
         ↓
┌─────────────────┐
│   5. Develop    │ ← Varias features acumuladas
│   → staging     │
└────────┬────────┘
         │
         │ QA Testing
         ↓
┌─────────────────┐
│   6. Staging    │ ← QA Sign-off
│   → main        │
└────────┬────────┘

Día 8: Release
         │
         ↓
┌─────────────────┐
│   7. Tag y      │ ← git tag v1.2.0
│   Release       │ ← 🎉 En Producción!
└─────────────────┘
```

## 🚨 Flujo de Hotfix (Emergencia)

```
    🔥 BUG CRÍTICO EN PRODUCCIÓN 🔥

┌────────────────────────────────────────┐
│              main (v1.2.0)             │ ← Bug detectado
└────────────────┬───────────────────────┘
                 │
                 │ Crear hotfix
                 ↓
            ┌─────────┐
            │hotfix/  │
            │bug-xxx  │ ← Fix rápido
            └────┬────┘
                 │
                 │ Test urgente
                 ↓
    ┌────────────────────────┐
    │    PR urgente a main   │ ← Merge inmediato
    └───────────┬────────────┘
                │
                ↓
┌───────────────────────────────────────┐
│         main (v1.2.1)                 │ ← Deploy urgente
│         + tag v1.2.1                  │
└───────────────┬───────────────────────┘
                │
                │ Sincronizar
                ↓
┌───────────────────────────────────────┐
│              develop                  │ ← Merge también aquí
└───────────────────────────────────────┘

⏱️ Tiempo total: 1-4 horas (vs días para feature normal)
```

## 📅 Timeline Típico (Sprint de 2 Semanas)

```
Semana 1:
├── Lunes-Miércoles: Desarrollo en feature branches
│   └── Múltiples features en paralelo
├── Jueves: Code review y merge a develop
└── Viernes: Integration testing en develop

Semana 2:
├── Lunes: Merge develop → staging
├── Martes-Jueves: QA testing en staging
└── Viernes: Release
    ├── Merge staging → main
    ├── Tag v1.x.0
    └── Deploy a producción 🚀
```

## 🎯 Estados de Protección

```
┌─────────────────────────────────────────────────────┐
│                    main                             │
│  🔒 Protección MÁXIMA                               │
│  • 2 revisores requeridos                           │
│  • CI/CD debe pasar                                 │
│  • Branch up-to-date                                │
│  • Solo tech leads pueden aprobar                   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                  staging                            │
│  🔒 Protección ALTA                                 │
│  • 1 revisor (QA) requerido                         │
│  • Tests de integración deben pasar                 │
│  • QA sign-off necesario                            │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                  develop                            │
│  🔒 Protección MEDIA                                │
│  • 1 revisor requerido                              │
│  • Tests unitarios deben pasar                      │
│  • PR template completo                             │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                 feature/*                           │
│  🔓 Sin protección                                   │
│  • Desarrollo libre                                 │
│  • Push directo permitido                           │
│  • Borrar después de merge                          │
└─────────────────────────────────────────────────────┘
```

## 📊 Ejemplo de Releases

```
main:     v1.0.0 ──────── v1.1.0 ──── v1.1.1 ─────── v2.0.0
          (inicial)       (feature)   (hotfix)       (major)
             │               │            │              │
             │               │            │              │
staging:     │     ●─────●   │    ●       │      ●────●  │
             │     Testing   │   Bug fix  │     Testing  │
             │               │            │              │
develop:  ●──●────●────●────●────●───●───●─────●────●───●
          │  Features      │    │  Hotfix│     Features │
          │  dev           │    │  merge │     dev      │
          │                │    │        │              │
features: ●──●  ●───●  ●───●    │        ●──●  ●────●   ●
          auth  api   rag       │        ui   payment   search
                                │
                            🔥 Hotfix
```

## 🔀 Merge Strategy

### Feature → Develop

```bash
Strategy: Squash and Merge
Result: 1 commit limpio en develop
Ventajas:
  ✅ Historial limpio
  ✅ Fácil de revertir
  ✅ PR = 1 commit
```

### Develop → Staging

```bash
Strategy: Merge Commit
Result: Preserva historial de features
Ventajas:
  ✅ Trazabilidad completa
  ✅ Ver qué features se incluyeron
  ✅ Fácil cherry-pick si necesario
```

### Staging → Main

```bash
Strategy: Merge Commit + Tag
Result: Release oficial con tag
Ventajas:
  ✅ Historial completo
  ✅ Versión trackeada
  ✅ Rollback fácil
```

## 🎨 Código de Colores (para Git Graph)

```
🟢 main      - Verde   (producción estable)
🟡 staging   - Amarillo (en pruebas)
🔵 develop   - Azul    (desarrollo activo)
🟣 feature/* - Púrpura (features individuales)
🔴 hotfix/*  - Rojo    (correcciones urgentes)
```

## 📈 Métricas de Éxito

```
┌─────────────────────────────────────┐
│  Métrica            │  Target       │
├─────────────────────┼───────────────┤
│  Deploy frequency   │  1x/semana    │
│  Lead time          │  < 1 semana   │
│  MTTR (hotfix)      │  < 4 horas    │
│  Failed deploys     │  < 5%         │
│  PR review time     │  < 24 horas   │
└─────────────────────┴───────────────┘
```

## 🛠️ Herramientas Visuales

### Ver Git Graph en VSCode

1. Instalar extensión "Git Graph"
2. Click en "Git Graph" en la barra inferior
3. Ver todas las ramas visualmente

### Ver en Terminal

```bash
# Graph completo
git log --all --graph --decorate --oneline

# Últimos 20 commits
git log --all --graph --decorate --oneline -20

# Solo ramas principales
git log --graph --oneline main staging develop
```

## 🔍 Comandos Útiles de Visualización

```bash
# Ver estado de todas las ramas
git branch -avv

# Ver ramas remotas
git branch -r

# Ver último commit de cada rama
git branch -v

# Ver ramas mergeadas a develop
git branch --merged develop

# Ver ramas no mergeadas
git branch --no-merged develop

# Ver diferencias entre ramas
git log develop..staging --oneline
git diff develop..staging

# Ver quién hizo qué
git shortlog -sn --all --since="1 month ago"
```

## 📚 Recursos Adicionales

- 📖 [Git Flow Cheatsheet](https://danielkummer.github.io/git-flow-cheatsheet/)
- 🎮 [Learn Git Branching (Interactive)](https://learngitbranching.js.org/)
- 📘 [Pro Git Book](https://git-scm.com/book/en/v2)

---

**💡 Tip**: Usa `git config --global alias.graph "log --all --graph --decorate --oneline"` para crear un alias y ejecutar simplemente `git graph`

**🎨 Tip**: Configura colores con `git config --global color.ui auto` para mejor visualización

---

**Última actualización**: 2025-10-06
