# Scripts de Utilidad

Este directorio contiene scripts útiles para el mantenimiento del proyecto.

## 📝 Scripts Disponibles

### 🌳 setup_branches

Inicializa la estructura de ramas Git del proyecto.

**Windows:**

```bash
scripts\setup_branches.bat
```

**Linux/Mac:**

```bash
chmod +x scripts/setup_branches.sh
./scripts/setup_branches.sh
```

**Python directo:**

```bash
python scripts/setup_branches.py
```

#### Lo que hace:

1. Verifica que estés en un repositorio Git válido
2. Crea las ramas `develop` y `staging` desde `main`
3. Pushea las ramas al repositorio remoto
4. Muestra instrucciones para configurar protección de ramas
5. Retorna a tu rama original

#### Requisitos:

- Git instalado y configurado
- Repositorio con al menos un commit
- Acceso de escritura al repositorio remoto

---

### 🔍 validate_docs (Por implementar)

Valida que la documentación esté sincronizada y completa.

```bash
python scripts/validate_docs.py
```

---

### 🏷️ create_release (Por implementar)

Automatiza la creación de releases.

```bash
python scripts/create_release.py --version v1.2.0
```

---

## 🛠️ Desarrollo de Nuevos Scripts

Al crear nuevos scripts:

1. **Usa Python** para lógica compleja
2. **Crea wrappers** .bat y .sh para facilitar ejecución
3. **Documenta** el propósito y uso en este README
4. **Agrega ayuda** con argparse o similar
5. **Maneja errores** gracefully
6. **Prueba** en Windows y Linux si es posible

### Template de Script

```python
#!/usr/bin/env python3
"""
Descripción breve del script
"""
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Descripción del script"
    )
    parser.add_argument(
        "--param",
        help="Descripción del parámetro"
    )
    args = parser.parse_args()

    # Lógica del script
    try:
        # ... código ...
        print("✅ Operación exitosa")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## 📞 Soporte

Si encuentras problemas con los scripts, abre un issue en el repositorio.
