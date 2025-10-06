# Healthcheck Script para Docker
# Este script verifica que la aplicación esté respondiendo correctamente

import sys
import requests
from time import sleep

def check_health(max_retries=3, delay=2):
    """Verificar el estado de salud de la aplicación"""
    
    endpoints = [
        ("http://localhost:8000/health", "API Health"),
        ("http://localhost:8000/docs", "API Docs"),
    ]
    
    for url, name in endpoints:
        for attempt in range(max_retries):
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ {name}: OK")
                    break
                else:
                    print(f"⚠️  {name}: Status {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"❌ {name}: Error - {str(e)}")
                if attempt < max_retries - 1:
                    print(f"   Reintentando en {delay}s...")
                    sleep(delay)
                else:
                    return False
    
    return True

if __name__ == "__main__":
    if check_health():
        print("\n🎉 Todos los servicios están operativos")
        sys.exit(0)
    else:
        print("\n💥 Algunos servicios fallaron")
        sys.exit(1)
