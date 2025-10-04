"""
Script simple para ejecutar solo la UI en modo API
"""

import os
import sys
from pathlib import Path

# Configurar environment para usar API
os.environ["API_BASE_URL"] = "http://localhost:8000"
os.environ["GRADIO_PORT"] = "7860"

# Configurar PYTHONPATH
project_root = Path(__file__).parent
os.environ["PYTHONPATH"] = str(project_root)

if __name__ == "__main__":
    print("🎨 Iniciando UI de Gradio...")
    print("🔗 Conectando con API en: http://localhost:8001")
    print("🎨 UI disponible en: http://localhost:7860")
    print("\n⚠️  Asegúrate de que la API esté corriendo en puerto 8001")
    
    # Importar y ejecutar la UI
    from api.ui_gradio import main
    main()