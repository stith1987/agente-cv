"""
Multi-LLM Demo

Demostración del sistema Multi-LLM plug-and-play que permite
invocar diferentes proveedores (DeepSeek, Groq, Gemini, Ollama, etc.)
usando la misma interfaz compatible con OpenAI.
"""

import os
import asyncio
from dotenv import load_dotenv

from agent.utils.multi_llm_client import (
    MultiLLMClient,
    MultiLLMEnsemble,
    create_multi_llm_client
)
from agent.utils.config import OpenAIConfig

load_dotenv()


def demo_single_provider():
    """Demo 1: Uso básico con un solo proveedor"""
    print("=" * 60)
    print("DEMO 1: Cliente único - OpenAI")
    print("=" * 60)
    
    # Crear cliente para OpenAI (default)
    client = create_multi_llm_client(
        provider="openai",
        model="gpt-3.5-turbo",
        temperature=0.7
    )
    
    messages = [
        {"role": "system", "content": "Eres un asistente técnico experto."},
        {"role": "user", "content": "Explica en 2 líneas qué es Docker"}
    ]
    
    print("\n📤 Enviando consulta...")
    response = client.generate(messages)
    
    print(f"\n✅ Respuesta de {response.provider} ({response.model}):")
    print(f"   {response.content}")
    print(f"   Tokens: {response.tokens_used}")
    print()


def demo_alternative_provider():
    """Demo 2: Uso con proveedor alternativo (DeepSeek ejemplo)"""
    print("=" * 60)
    print("DEMO 2: Proveedor alternativo - DeepSeek")
    print("=" * 60)
    
    # Verificar si hay API key configurada
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    if not deepseek_key:
        print("\n⚠️  DEEPSEEK_API_KEY no configurada")
        print("   Para usar DeepSeek, configura en .env:")
        print("   DEEPSEEK_API_KEY=tu_clave_aqui")
        print("\n   Simulando configuración...\n")
        return
    
    # Crear cliente para DeepSeek
    client = create_multi_llm_client(
        provider="deepseek",
        api_key=deepseek_key,
        model="deepseek-chat",
        temperature=0.7
    )
    
    messages = [
        {"role": "system", "content": "Eres un asistente útil."},
        {"role": "user", "content": "¿Cuál es la capital de Francia?"}
    ]
    
    print("\n📤 Enviando consulta a DeepSeek...")
    try:
        response = client.generate(messages)
        print(f"\n✅ Respuesta de {response.provider}:")
        print(f"   {response.content}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    print()


def demo_groq_provider():
    """Demo 3: Uso con Groq (Mixtral, Llama)"""
    print("=" * 60)
    print("DEMO 3: Groq - Mixtral/Llama")
    print("=" * 60)
    
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        print("\n⚠️  GROQ_API_KEY no configurada")
        print("   Para usar Groq, configura en .env:")
        print("   GROQ_API_KEY=tu_clave_aqui")
        print("\n   Modelos disponibles:")
        print("   - mixtral-8x7b-32768")
        print("   - llama-3.1-70b-versatile")
        print("   - gemma-7b-it\n")
        return
    
    client = create_multi_llm_client(
        provider="groq",
        api_key=groq_key,
        model="mixtral-8x7b-32768",
        temperature=0.7
    )
    
    messages = [
        {"role": "system", "content": "Eres un experto en IA."},
        {"role": "user", "content": "¿Qué es un transformer en Deep Learning?"}
    ]
    
    print("\n📤 Enviando consulta a Groq (Mixtral)...")
    try:
        response = client.generate(messages)
        print(f"\n✅ Respuesta de {response.provider} ({response.model}):")
        print(f"   {response.content[:200]}...")
        print(f"   Tokens: {response.tokens_used}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    print()


async def demo_ensemble():
    """Demo 4: Sistema de Ensemble - múltiples modelos en paralelo"""
    print("=" * 60)
    print("DEMO 4: Ensemble Multi-LLM")
    print("=" * 60)
    
    # Configurar múltiples proveedores
    # Nota: Usa solo los que tengas configurados
    configs = []
    
    # OpenAI (siempre disponible si tienes key)
    if os.getenv("OPENAI_API_KEY"):
        configs.append(
            OpenAIConfig(
                api_key=os.getenv("OPENAI_API_KEY"),
                model="gpt-3.5-turbo",
                provider="openai",
                temperature=0.7,
                max_tokens=500
            )
        )
    
    # DeepSeek
    if os.getenv("DEEPSEEK_API_KEY"):
        configs.append(
            OpenAIConfig(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                model="deepseek-chat",
                provider="deepseek",
                temperature=0.7,
                max_tokens=500
            )
        )
    
    # Groq
    if os.getenv("GROQ_API_KEY"):
        configs.append(
            OpenAIConfig(
                api_key=os.getenv("GROQ_API_KEY"),
                model="mixtral-8x7b-32768",
                provider="groq",
                temperature=0.7,
                max_tokens=500
            )
        )
    
    if not configs:
        print("\n⚠️  No hay proveedores configurados para ensemble")
        print("   Configura al menos 2 proveedores en .env:")
        print("   - OPENAI_API_KEY")
        print("   - DEEPSEEK_API_KEY")
        print("   - GROQ_API_KEY")
        return
    
    if len(configs) < 2:
        print("\n⚠️  Ensemble requiere al menos 2 proveedores")
        print(f"   Solo tienes {len(configs)} configurado")
        return
    
    print(f"\n🚀 Creando ensemble con {len(configs)} proveedores:")
    for config in configs:
        print(f"   - {config.provider} ({config.model})")
    
    ensemble = MultiLLMEnsemble(configs)
    
    messages = [
        {"role": "system", "content": "Eres un experto en arquitectura de software."},
        {"role": "user", "content": "Explica el patrón de microservicios en 3 puntos"}
    ]
    
    print("\n📤 Enviando consulta a todos los modelos en paralelo...")
    
    try:
        responses = await ensemble.generate_ensemble(messages)
        
        print(f"\n✅ Recibidas {len(responses)} respuestas:")
        print()
        
        for i, response in enumerate(responses, 1):
            print(f"{i}. {response.provider} ({response.model}):")
            print(f"   {response.content[:150]}...")
            print(f"   Tokens: {response.tokens_used}")
            print()
        
        # Seleccionar mejor respuesta
        print("🏆 Seleccionando mejor respuesta (por longitud)...")
        best = ensemble.select_best_response(responses, criteria="length")
        print(f"   Ganador: {best.provider} con {len(best.content)} caracteres")
        print()
        
        # Combinar respuestas
        print("🔀 Combinando todas las respuestas...")
        combined = ensemble.combine_responses(responses)
        print(f"   Respuesta combinada ({len(combined)} caracteres):")
        print(f"   {combined[:200]}...")
        print()
        
    except Exception as e:
        print(f"\n❌ Error en ensemble: {e}")
    
    print()


def demo_configuration():
    """Demo 5: Diferentes configuraciones de temperatura y tokens"""
    print("=" * 60)
    print("DEMO 5: Configuraciones personalizadas")
    print("=" * 60)
    
    client = create_multi_llm_client(
        provider="openai",
        model="gpt-3.5-turbo"
    )
    
    messages = [
        {"role": "system", "content": "Eres un poeta."},
        {"role": "user", "content": "Escribe un haiku sobre el código"}
    ]
    
    print("\n📝 Probando diferentes temperaturas...")
    
    for temp in [0.2, 0.7, 1.2]:
        print(f"\n   Temperature = {temp}:")
        response = client.generate(messages, temperature=temp, max_tokens=100)
        print(f"   {response.content}")
    
    print()


def print_provider_examples():
    """Mostrar ejemplos de configuración para diferentes proveedores"""
    print("=" * 60)
    print("EJEMPLOS DE CONFIGURACIÓN POR PROVEEDOR")
    print("=" * 60)
    
    examples = {
        "OpenAI": {
            "env": ["OPENAI_API_KEY=sk-...", "OPENAI_MODEL=gpt-4"],
            "code": """client = create_multi_llm_client(
    provider="openai",
    model="gpt-4"
)"""
        },
        "DeepSeek": {
            "env": ["DEEPSEEK_API_KEY=sk-...", "OPENAI_MODEL=deepseek-chat"],
            "code": """client = create_multi_llm_client(
    provider="deepseek",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    model="deepseek-chat"
)"""
        },
        "Groq": {
            "env": ["GROQ_API_KEY=gsk_...", "OPENAI_MODEL=mixtral-8x7b-32768"],
            "code": """client = create_multi_llm_client(
    provider="groq",
    api_key=os.getenv("GROQ_API_KEY"),
    model="mixtral-8x7b-32768"
)"""
        },
        "Ollama": {
            "env": ["# No requiere API key", "OPENAI_MODEL=llama3.1"],
            "code": """client = create_multi_llm_client(
    provider="ollama",
    api_key="ollama",  # Cualquier string
    model="llama3.1",
    base_url="http://localhost:11434/v1"
)"""
        }
    }
    
    for provider, info in examples.items():
        print(f"\n🔹 {provider}:")
        print("   Variables .env:")
        for var in info["env"]:
            print(f"      {var}")
        print("\n   Código Python:")
        for line in info["code"].split("\n"):
            print(f"      {line}")
    
    print("\n")


def main():
    """Ejecutar todas las demos"""
    print("\n")
    print("🤖 " + "=" * 58)
    print("🤖  MULTI-LLM PLUG-AND-PLAY DEMO")
    print("🤖 " + "=" * 58)
    print()
    
    # Mostrar configuración actual
    print("📋 Configuración detectada:")
    print(f"   OPENAI_API_KEY: {'✅ Configurada' if os.getenv('OPENAI_API_KEY') else '❌ No configurada'}")
    print(f"   DEEPSEEK_API_KEY: {'✅ Configurada' if os.getenv('DEEPSEEK_API_KEY') else '❌ No configurada'}")
    print(f"   GROQ_API_KEY: {'✅ Configurada' if os.getenv('GROQ_API_KEY') else '❌ No configurada'}")
    print()
    
    try:
        # Demos síncronos
        demo_single_provider()
        demo_alternative_provider()
        demo_groq_provider()
        demo_configuration()
        
        # Demo asíncrono (ensemble)
        if os.getenv("OPENAI_API_KEY"):
            asyncio.run(demo_ensemble())
        
        # Ejemplos de configuración
        print_provider_examples()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrumpida por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error en demo: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)
    print("✅ Demo completada")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
