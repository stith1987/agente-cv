"""
Script para probar Multi-LLM en el contenedor Docker
"""

import requests
import json

API_URL = "http://localhost:8000"

def test_health():
    """Probar endpoint de health"""
    print("\n=== TEST HEALTH ===")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_chat(message: str):
    """Probar endpoint de chat"""
    print(f"\n=== TEST CHAT ===")
    print(f"Pregunta: {message}")
    
    payload = {
        "message": message,
        "session_id": "test-multi-llm",
        "notify_important": False,
        "evaluate_response": False
    }
    
    response = requests.post(f"{API_URL}/chat", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nRespuesta: {data.get('response', 'N/A')[:200]}...")
        
        metadata = data.get('metadata', {})
        print(f"\n--- Metadata ---")
        print(f"Provider: {metadata.get('provider', 'N/A')}")
        print(f"Model: {metadata.get('model', 'N/A')}")
        print(f"Tokens: {metadata.get('tokens', 'N/A')}")
        print(f"Cost: ${metadata.get('cost', 0):.6f}")
        
        return True
    else:
        print(f"Error: {response.text}")
        return False

def main():
    """Ejecutar todos los tests"""
    print("🚀 Probando Multi-LLM en Docker Container")
    print("=" * 60)
    
    # Test 1: Health
    if not test_health():
        print("\n❌ Health check falló")
        return
    
    # Test 2: Chat básico
    test_chat("Hola, ¿qué proveedor LLM estás usando?")
    
    # Test 3: Pregunta sobre CV
    test_chat("¿Cuáles son las habilidades técnicas de Eduardo?")
    
    print("\n" + "=" * 60)
    print("✅ Tests completados")

if __name__ == "__main__":
    main()
