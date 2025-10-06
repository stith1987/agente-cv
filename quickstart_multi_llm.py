#!/usr/bin/env python
"""
Quick Start - Multi-LLM

Script de inicio rápido para probar el Multi-LLM Client
"""

import os
from dotenv import load_dotenv

load_dotenv()


def show_status():
    """Mostrar estado de configuración"""
    print("\n" + "=" * 60)
    print("🤖 MULTI-LLM PLUG-AND-PLAY - QUICK START")
    print("=" * 60 + "\n")
    
    # Detectar proveedores configurados
    providers = {
        "OpenAI": os.getenv("OPENAI_API_KEY"),
        "DeepSeek": os.getenv("DEEPSEEK_API_KEY"),
        "Groq": os.getenv("GROQ_API_KEY"),
    }
    
    print("📋 Estado de Configuración:\n")
    for provider, key in providers.items():
        status = "✅ Configurado" if key else "❌ No configurado"
        print(f"   {provider:12s}: {status}")
    
    print("\n" + "=" * 60)
    print("📚 Recursos Disponibles:")
    print("=" * 60 + "\n")
    
    resources = {
        "Guía completa": "docs/MULTI_LLM_GUIDE.md",
        "Demo interactiva": "python examples/multi_llm_demo.py",
        "Resumen implementación": "IMPLEMENTATION_MULTI_LLM.md",
        "Configuración": ".env.example"
    }
    
    for name, path in resources.items():
        print(f"   📄 {name:25s}: {path}")
    
    print("\n" + "=" * 60)
    print("🚀 Uso Rápido:")
    print("=" * 60 + "\n")
    
    print("""   # 1. Configurar provider en .env
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sk-...
   
   # 2. Usar en código
   from agent.utils.multi_llm_client import create_multi_llm_client
   
   client = create_multi_llm_client(provider="openai")
   response = client.generate([
       {"role": "user", "content": "Hello!"}
   ])
   print(response.content)
   
   # 3. O usar con CVOrchestrator
   from agent.core.orchestrator import CVOrchestrator
   
   orchestrator = CVOrchestrator()
   result = orchestrator.process_query("¿Cuáles son mis proyectos?")
""")
    
    print("\n" + "=" * 60)
    print("💡 Proveedores Soportados:")
    print("=" * 60 + "\n")
    
    providers_info = [
        ("OpenAI", "GPT-4, GPT-3.5", "Máxima calidad"),
        ("DeepSeek", "deepseek-chat", "Económico (~99% más barato)"),
        ("Groq", "Mixtral, Llama", "Ultra rápido (gratis)"),
        ("Ollama", "Llama, Mistral", "Local (sin API key)")
    ]
    
    for provider, models, note in providers_info:
        print(f"   🔹 {provider:10s}: {models:20s} - {note}")
    
    print("\n" + "=" * 60)
    print("📖 Siguiente Paso:")
    print("=" * 60 + "\n")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("   ⚠️  Configura OPENAI_API_KEY en .env")
        print("   📝 Copia .env.example a .env y añade tu API key\n")
    else:
        print("   ✅ Configuración lista!")
        print("   🎯 Ejecuta: python examples/multi_llm_demo.py\n")


def test_basic():
    """Test básico de funcionalidad"""
    print("\n" + "=" * 60)
    print("🧪 Test de Funcionalidad Básica")
    print("=" * 60 + "\n")
    
    try:
        from agent.utils.multi_llm_client import create_multi_llm_client
        print("   ✅ Imports exitosos")
        
        # Solo test de creación, no llamada real
        api_key = os.getenv("OPENAI_API_KEY", "test-key")
        client = create_multi_llm_client(
            provider="openai",
            api_key=api_key,
            model="gpt-3.5-turbo"
        )
        print("   ✅ Cliente creado correctamente")
        
        print("\n   🎉 Multi-LLM Client está funcionando!\n")
        
        if api_key == "test-key":
            print("   ℹ️  Configura OPENAI_API_KEY para hacer llamadas reales\n")
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")


if __name__ == "__main__":
    show_status()
    test_basic()
    
    print("=" * 60)
    print("✨ Listo para usar Multi-LLM!")
    print("=" * 60 + "\n")
