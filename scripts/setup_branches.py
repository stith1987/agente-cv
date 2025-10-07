#!/usr/bin/env python3
"""
Script para inicializar la estructura de ramas Git
"""
import subprocess
import sys
from typing import List, Tuple

def run_command(command: List[str]) -> Tuple[bool, str]:
    """Ejecuta un comando y retorna (success, output)"""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def create_branch(branch_name: str, from_branch: str = "main") -> bool:
    """Crea una nueva rama desde otra rama"""
    print(f"📝 Creando rama: {branch_name} desde {from_branch}...")
    
    # Asegurar que estamos en la rama correcta
    success, _ = run_command(["git", "checkout", from_branch])
    if not success:
        print(f"❌ Error: No se pudo cambiar a la rama {from_branch}")
        return False
    
    # Actualizar la rama base
    success, _ = run_command(["git", "pull", "origin", from_branch])
    if not success:
        print(f"⚠️ Advertencia: No se pudo hacer pull de {from_branch}")
    
    # Crear la nueva rama
    success, _ = run_command(["git", "checkout", "-b", branch_name])
    if not success:
        # Si la rama ya existe, solo hacer checkout
        success, _ = run_command(["git", "checkout", branch_name])
        if success:
            print(f"ℹ️ La rama {branch_name} ya existía, cambiando a ella...")
        else:
            print(f"❌ Error: No se pudo crear o cambiar a {branch_name}")
            return False
    
    # Pushear la nueva rama
    success, _ = run_command(["git", "push", "-u", "origin", branch_name])
    if not success:
        print(f"⚠️ Advertencia: No se pudo pushear {branch_name} al remoto")
        print(f"   Ejecuta manualmente: git push -u origin {branch_name}")
    else:
        print(f"✅ Rama {branch_name} creada y pusheada exitosamente")
    
    return True

def setup_branch_protection():
    """Muestra instrucciones para configurar protección de ramas"""
    print("\n🔒 CONFIGURACIÓN DE PROTECCIÓN DE RAMAS")
    print("=" * 60)
    print("\nPara configurar la protección de ramas en GitHub:")
    print("\n1. Ve a tu repositorio en GitHub")
    print("2. Settings → Branches → Add rule")
    print("\n📌 Para la rama 'main':")
    print("   - Branch name pattern: main")
    print("   - ✅ Require a pull request before merging")
    print("   - ✅ Require approvals: 2")
    print("   - ✅ Require status checks to pass")
    print("   - ✅ Require branches to be up to date")
    print("   - ✅ Include administrators")
    print("\n📌 Para la rama 'staging':")
    print("   - Branch name pattern: staging")
    print("   - ✅ Require a pull request before merging")
    print("   - ✅ Require approvals: 1")
    print("   - ✅ Require status checks to pass")
    print("\n📌 Para la rama 'develop':")
    print("   - Branch name pattern: develop")
    print("   - ✅ Require a pull request before merging")
    print("   - ✅ Require approvals: 1")

def main():
    """Función principal"""
    print("🚀 INICIALIZANDO ESTRUCTURA DE RAMAS GIT")
    print("=" * 60)
    
    # Verificar que estamos en un repositorio git
    success, _ = run_command(["git", "rev-parse", "--git-dir"])
    if not success:
        print("❌ Error: No estás en un repositorio Git")
        sys.exit(1)
    
    # Obtener rama actual
    success, output = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    if not success:
        print("❌ Error: No se pudo obtener la rama actual")
        sys.exit(1)
    
    current_branch = output.strip()
    print(f"📍 Rama actual: {current_branch}")
    
    # Asegurar que hay commits
    success, _ = run_command(["git", "log", "-1"])
    if not success:
        print("❌ Error: El repositorio no tiene commits")
        print("   Realiza al menos un commit antes de ejecutar este script")
        sys.exit(1)
    
    # Confirmar con el usuario
    print("\n⚠️ Este script creará las siguientes ramas:")
    print("   - develop (desde main)")
    print("   - staging (desde main)")
    print("\n¿Deseas continuar? (s/n): ", end="")
    
    response = input().lower()
    if response != 's':
        print("❌ Operación cancelada")
        sys.exit(0)
    
    # Crear ramas
    branches = [
        ("develop", "main"),
        ("staging", "main"),
    ]
    
    success_count = 0
    for branch_name, from_branch in branches:
        if create_branch(branch_name, from_branch):
            success_count += 1
        print()
    
    # Volver a la rama original
    print(f"🔙 Volviendo a la rama original: {current_branch}")
    run_command(["git", "checkout", current_branch])
    
    # Resumen
    print("\n" + "=" * 60)
    print(f"✅ RESUMEN: {success_count}/{len(branches)} ramas creadas exitosamente")
    print("=" * 60)
    
    # Mostrar estructura de ramas
    print("\n🌳 Estructura de ramas:")
    success, output = run_command(["git", "branch", "-a"])
    if success:
        print(output)
    
    # Instrucciones de protección
    setup_branch_protection()
    
    print("\n📚 PRÓXIMOS PASOS:")
    print("1. Configura la protección de ramas en GitHub (ver arriba)")
    print("2. Revisa GIT_WORKFLOW.md para el flujo de trabajo completo")
    print("3. Empieza a trabajar en una feature branch:")
    print("   git checkout develop")
    print("   git checkout -b feature/mi-nueva-caracteristica")
    print("\n✨ ¡Listo! Tu estructura de ramas está configurada.")

if __name__ == "__main__":
    main()
