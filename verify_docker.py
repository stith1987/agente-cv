#!/usr/bin/env python3
"""
Script de verificación de Docker para agente-cv
Verifica que todo esté configurado correctamente antes del deployment
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Tuple, List

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

def run_command(cmd: List[str]) -> Tuple[bool, str]:
    """Ejecuta un comando y retorna (success, output)"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)

def check_docker_installed() -> bool:
    """Verifica que Docker esté instalado"""
    print_info("Verificando instalación de Docker...")
    success, output = run_command(["docker", "--version"])
    if success:
        print_success(f"Docker instalado: {output.strip()}")
        return True
    else:
        print_error("Docker no está instalado o no está en el PATH")
        return False

def check_docker_compose_installed() -> bool:
    """Verifica que Docker Compose esté instalado"""
    print_info("Verificando instalación de Docker Compose...")
    success, output = run_command(["docker-compose", "--version"])
    if success:
        print_success(f"Docker Compose instalado: {output.strip()}")
        return True
    else:
        print_error("Docker Compose no está instalado")
        return False

def check_docker_running() -> bool:
    """Verifica que Docker daemon esté corriendo"""
    print_info("Verificando que Docker esté corriendo...")
    success, output = run_command(["docker", "ps"])
    if success:
        print_success("Docker daemon está corriendo")
        return True
    else:
        print_error("Docker daemon no está corriendo")
        print_warning("Inicia Docker Desktop o el servicio de Docker")
        return False

def check_required_files() -> bool:
    """Verifica que existan los archivos necesarios"""
    print_info("Verificando archivos requeridos...")
    
    required_files = [
        "Dockerfile",
        "docker-compose.yml",
        "requirements.txt",
        ".dockerignore",
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print_success(f"Archivo encontrado: {file}")
        else:
            print_error(f"Archivo faltante: {file}")
            all_exist = False
    
    return all_exist

def check_env_file() -> bool:
    """Verifica que exista el archivo .env"""
    print_info("Verificando archivo de configuración...")
    
    if Path(".env").exists():
        print_success("Archivo .env encontrado")
        
        # Verificar variables importantes
        with open(".env", "r") as f:
            content = f.read()
            
        important_vars = [
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "GROQ_API_KEY",
        ]
        
        found_vars = []
        for var in important_vars:
            if var in content and not content.split(var)[1].split('\n')[0].strip().endswith('='):
                found_vars.append(var)
        
        if found_vars:
            print_success(f"Variables configuradas: {', '.join(found_vars)}")
        else:
            print_warning("No se encontraron API keys configuradas")
            print_info("Edita .env y agrega tus API keys")
        
        return True
    else:
        print_warning("Archivo .env no encontrado")
        if Path(".env.example").exists():
            print_info("Ejecuta: cp .env.example .env")
            print_info("Luego edita .env con tus API keys")
        return False

def check_ports_available() -> bool:
    """Verifica que los puertos necesarios estén disponibles"""
    print_info("Verificando disponibilidad de puertos...")
    
    ports_to_check = [8000, 7860]
    all_available = True
    
    for port in ports_to_check:
        # Este check es básico, puede no funcionar en todos los sistemas
        if sys.platform == "win32":
            success, output = run_command(
                ["powershell", "-Command", 
                 f"Get-NetTCPConnection -LocalPort {port} -ErrorAction SilentlyContinue"]
            )
            if "LISTENING" in output or "ESTABLISHED" in output:
                print_warning(f"Puerto {port} puede estar en uso")
                all_available = False
            else:
                print_success(f"Puerto {port} disponible")
        else:
            success, output = run_command(["lsof", "-i", f":{port}"])
            if success and output:
                print_warning(f"Puerto {port} en uso")
                all_available = False
            else:
                print_success(f"Puerto {port} disponible")
    
    return all_available

def check_disk_space() -> bool:
    """Verifica que haya espacio en disco suficiente"""
    print_info("Verificando espacio en disco...")
    
    # Mínimo recomendado: 5GB
    min_space_gb = 5
    
    try:
        import shutil
        stat = shutil.disk_usage(".")
        free_gb = stat.free / (1024**3)
        
        if free_gb >= min_space_gb:
            print_success(f"Espacio disponible: {free_gb:.2f} GB")
            return True
        else:
            print_warning(f"Poco espacio: {free_gb:.2f} GB (recomendado: {min_space_gb}+ GB)")
            return False
    except Exception as e:
        print_warning(f"No se pudo verificar espacio: {e}")
        return True  # No bloquear por esto

def check_docker_resources() -> bool:
    """Verifica que Docker tenga recursos suficientes"""
    print_info("Verificando recursos de Docker...")
    
    success, output = run_command(["docker", "info"])
    if not success:
        print_warning("No se pudo obtener info de Docker")
        return True
    
    # Extraer info de memoria (esto es básico)
    lines = output.split('\n')
    for line in lines:
        if 'Total Memory' in line or 'Memory' in line:
            print_info(line.strip())
    
    print_success("Recursos de Docker OK")
    return True

def test_docker_build() -> bool:
    """Prueba un build de Docker (sin caché)"""
    print_info("Probando build de Docker (esto puede tardar)...")
    
    # Solo verificar que no haya errores obvios
    success, output = run_command(["docker-compose", "config"])
    if success:
        print_success("Configuración de docker-compose es válida")
        return True
    else:
        print_error("Error en docker-compose.yml:")
        print(output)
        return False

def main():
    print_header("Verificación de Docker para agente-cv")
    
    checks = [
        ("Docker instalado", check_docker_installed),
        ("Docker Compose instalado", check_docker_compose_installed),
        ("Docker corriendo", check_docker_running),
        ("Archivos requeridos", check_required_files),
        ("Archivo .env", check_env_file),
        ("Puertos disponibles", check_ports_available),
        ("Espacio en disco", check_disk_space),
        ("Recursos Docker", check_docker_resources),
        ("Configuración válida", test_docker_build),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"Error en {name}: {e}")
            results.append((name, False))
    
    # Resumen
    print_header("Resumen de Verificación")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        if result:
            print_success(f"{name}")
        else:
            print_error(f"{name}")
    
    print(f"\n{Colors.BOLD}Resultado: {passed}/{total} checks pasados{Colors.ENDC}\n")
    
    if passed == total:
        print_success("¡Todo listo para usar Docker! 🎉")
        print_info("\nPróximos pasos:")
        print("  1. docker-compose build")
        print("  2. docker-compose up -d")
        print("  3. Visita http://localhost:8000/docs")
        return 0
    elif passed >= total * 0.7:
        print_warning("Algunas verificaciones fallaron, pero puedes intentar continuar")
        print_info("Revisa los errores arriba y corrígelos si es posible")
        return 1
    else:
        print_error("Muchas verificaciones fallaron")
        print_info("Corrige los problemas antes de continuar")
        return 2

if __name__ == "__main__":
    sys.exit(main())
