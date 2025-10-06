"""
Script para ejecutar la API y la UI de Gradio
"""

import subprocess
import time
import os
import sys
from pathlib import Path

def main():
    """Ejecutar API y UI en paralelo"""
    
    # Configurar paths
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Configurar variables de entorno
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root)
    env["PORT"] = "8000"
    env["API_BASE_URL"] = "http://localhost:8000"
    env["GRADIO_PORT"] = "7860"
    
    print("🚀 Iniciando CV Agent con Frontend Multi-LLM...")
    print(f"📁 Directorio de trabajo: {project_root}")
    print(f"🔗 API URL: {env['API_BASE_URL']}")
    print(f"🎨 UI URL: http://localhost:{env['GRADIO_PORT']} (Multi-LLM)")
    
    try:
        # Ejecutar API en background
        print("\n📡 Iniciando API...")
        api_process = subprocess.Popen([
            sys.executable, "api/app.py"
        ], env=env, cwd=project_root)
        
        # Esperar a que la API se inicie
        print("⏳ Esperando a que la API se inicie...")
        time.sleep(5)
        
        # Ejecutar UI con Multi-LLM selector
        print("\n🎨 Iniciando UI de Gradio con Multi-LLM...")
        ui_process = subprocess.Popen([
            sys.executable, "api/ui_gradio_multi_llm.py"
        ], env=env, cwd=project_root)
        
        print("\n✅ ¡Ambos servicios iniciados!")
        print("🔗 API: http://localhost:8001")
        print("🔗 Docs: http://localhost:8001/docs")
        print("🎨 UI Multi-LLM: http://localhost:7860")
        print("💡 Selecciona el proveedor LLM desde el dropdown en la UI")
        print("\n👆 Abre http://localhost:7860 en tu navegador")
        print("⏹️  Presiona Ctrl+C para detener ambos servicios")
        
        # Esperar hasta que el usuario termine
        try:
            api_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo servicios...")
            
            # Terminar procesos
            try:
                api_process.terminate()
                api_process.wait(timeout=5)
            except:
                api_process.kill()
                
            try:
                ui_process.terminate()
                ui_process.wait(timeout=5)
            except:
                ui_process.kill()
                
            print("✅ Servicios detenidos")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())