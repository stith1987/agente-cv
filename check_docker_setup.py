#!/usr/bin/env python3
"""
Script para verificar la completitud de la implementación Docker
Valida que todos los archivos necesarios estén presentes y sean válidos
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text: str):
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")

def print_error(text: str):
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")

def print_warning(text: str):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")

def print_info(text: str):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.ENDC}")

def check_files() -> Tuple[List[str], List[str]]:
    """Verifica que existan todos los archivos necesarios"""
    
    required_files = {
        "Docker Core": [
            "Dockerfile",
            ".dockerignore",
            "docker-compose.yml",
            "docker-compose.dev.yml",
            "docker-compose.prod.yml",
            "docker-compose.scaled.yml",
        ],
        "Documentación": [
            "README_DOCKER.md",
            "DOCKER_SUMMARY.md",
            "DOCKER_BEST_PRACTICES.md",
            "DOCKER_TROUBLESHOOTING.md",
            "DOCKER_QUICK_REFERENCE.md",
        ],
        "Scripts": [
            "docker_manager.bat",
            "docker_manager.sh",
            "docker_quickstart.bat",
            "docker_quickstart.sh",
            "Makefile",
        ],
        "Utilidades": [
            "healthcheck.py",
            "verify_docker.py",
            "nginx.conf",
        ],
        "CI/CD": [
            ".github/workflows/docker-ci.yml",
            ".github/workflows/README.md",
        ],
        "Configuración": [
            ".env.example",
        ],
    }
    
    found = []
    missing = []
    
    print_header("Verificación de Archivos Docker")
    
    for category, files in required_files.items():
        print(f"\n{Colors.BOLD}{category}:{Colors.ENDC}")
        for file in files:
            path = Path(file)
            if path.exists():
                size = path.stat().st_size
                print_success(f"{file} ({size:,} bytes)")
                found.append(file)
            else:
                print_error(f"{file} - NO ENCONTRADO")
                missing.append(file)
    
    return found, missing

def check_file_contents():
    """Verifica el contenido básico de archivos clave"""
    print_header("Verificación de Contenido")
    
    checks = {
        "Dockerfile": ["FROM python", "WORKDIR /app", "COPY requirements.txt"],
        "docker-compose.yml": ["version:", "services:", "agente-cv:"],
        ".dockerignore": ["__pycache__", "*.pyc", ".git"],
        "README_DOCKER.md": ["# ", "Docker", "docker-compose"],
    }
    
    for file, required_content in checks.items():
        path = Path(file)
        if not path.exists():
            print_warning(f"Saltando {file} (no existe)")
            continue
        
        try:
            content = path.read_text(encoding='utf-8')
            missing_content = []
            
            for required in required_content:
                if required not in content:
                    missing_content.append(required)
            
            if missing_content:
                print_warning(f"{file} - Falta contenido: {', '.join(missing_content)}")
            else:
                print_success(f"{file} - Contenido válido")
        
        except Exception as e:
            print_error(f"{file} - Error al leer: {e}")

def check_readme_links():
    """Verifica que el README principal tenga enlaces a la documentación Docker"""
    print_header("Verificación de Enlaces en README")
    
    readme_path = Path("README.md")
    if not readme_path.exists():
        print_error("README.md no encontrado")
        return
    
    content = readme_path.read_text(encoding='utf-8')
    
    expected_links = [
        "DOCKER_SUMMARY.md",
        "README_DOCKER.md",
        "docker-compose",
    ]
    
    for link in expected_links:
        if link in content:
            print_success(f"Enlace a {link} encontrado")
        else:
            print_warning(f"Enlace a {link} no encontrado en README.md")

def check_scripts_executable():
    """Verifica que los scripts tengan permisos de ejecución (Unix)"""
    if sys.platform == "win32":
        print_info("Saltando verificación de permisos (Windows)")
        return
    
    print_header("Verificación de Permisos")
    
    scripts = [
        "docker_manager.sh",
        "docker_quickstart.sh",
    ]
    
    for script in scripts:
        path = Path(script)
        if not path.exists():
            print_warning(f"{script} no existe")
            continue
        
        if os.access(path, os.X_OK):
            print_success(f"{script} es ejecutable")
        else:
            print_warning(f"{script} no es ejecutable")
            print_info(f"  Ejecuta: chmod +x {script}")

def generate_structure_tree():
    """Genera un árbol de estructura de archivos Docker"""
    print_header("Estructura de Archivos Docker")
    
    docker_files = []
    
    # Archivos en raíz
    root_files = [
        "Dockerfile",
        ".dockerignore", 
        "docker-compose.yml",
        "docker-compose.dev.yml",
        "docker-compose.prod.yml",
        "docker-compose.scaled.yml",
        "Makefile",
        "nginx.conf",
        "healthcheck.py",
        "verify_docker.py",
    ]
    
    # Scripts
    script_files = [
        "docker_manager.bat",
        "docker_manager.sh",
        "docker_quickstart.bat",
        "docker_quickstart.sh",
    ]
    
    # Documentación
    doc_files = [
        "README_DOCKER.md",
        "DOCKER_SUMMARY.md",
        "DOCKER_BEST_PRACTICES.md",
        "DOCKER_TROUBLESHOOTING.md",
        "DOCKER_QUICK_REFERENCE.md",
    ]
    
    print("📦 agente-cv/")
    print("├── 🐳 Docker Core")
    for f in root_files:
        if Path(f).exists():
            print(f"│   ├── {f}")
    
    print("├── 📜 Scripts")
    for f in script_files:
        if Path(f).exists():
            print(f"│   ├── {f}")
    
    print("├── 📖 Documentación")
    for f in doc_files:
        if Path(f).exists():
            print(f"│   ├── {f}")
    
    print("└── 🔄 CI/CD")
    if Path(".github/workflows/docker-ci.yml").exists():
        print("    └── .github/workflows/docker-ci.yml")

def print_summary(found: List[str], missing: List[str]):
    """Imprime un resumen de la verificación"""
    print_header("Resumen")
    
    total = len(found) + len(missing)
    percentage = (len(found) / total * 100) if total > 0 else 0
    
    print(f"Archivos encontrados: {len(found)}/{total} ({percentage:.1f}%)")
    
    if missing:
        print(f"\n{Colors.RED}{Colors.BOLD}Archivos faltantes:{Colors.ENDC}")
        for file in missing:
            print(f"  - {file}")
    
    print()
    
    if percentage == 100:
        print_success("¡Implementación Docker completa! 🎉")
        print_info("\nPróximos pasos:")
        print("  1. Verifica la configuración: python verify_docker.py")
        print("  2. Construye las imágenes: docker-compose build")
        print("  3. Inicia los servicios: docker-compose up -d")
        return 0
    elif percentage >= 80:
        print_warning("Implementación casi completa")
        print_info("Revisa los archivos faltantes arriba")
        return 1
    else:
        print_error("Implementación incompleta")
        print_info("Faltan varios archivos importantes")
        return 2

def main():
    """Función principal"""
    print_header("Verificación de Implementación Docker")
    print_info("Verificando archivos y configuración...")
    
    # Verificar que estamos en el directorio correcto
    if not Path("requirements.txt").exists():
        print_error("No estás en el directorio del proyecto agente-cv")
        print_info("Navega al directorio del proyecto e intenta de nuevo")
        return 1
    
    # Verificar archivos
    found, missing = check_files()
    
    # Verificar contenido
    check_file_contents()
    
    # Verificar enlaces
    check_readme_links()
    
    # Verificar permisos
    check_scripts_executable()
    
    # Mostrar estructura
    generate_structure_tree()
    
    # Resumen
    return print_summary(found, missing)

if __name__ == "__main__":
    sys.exit(main())
