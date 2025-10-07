#!/usr/bin/env python
"""
Launch Multi-LLM UI

Script para lanzar la interfaz Gradio con selector de proveedores LLM
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.ui_gradio_multi_llm import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interfaz cerrada por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
