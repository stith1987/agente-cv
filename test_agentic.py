#!/usr/bin/env python3
"""
Test de funcionalidades agentic
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.orchestrator import CVOrchestrator

def test_clarification():
    """Test del proceso de clarificación"""
    print("🤔 Probando funcionalidad de clarificación...")
    
    orchestrator = CVOrchestrator()
    
    result = orchestrator.process_query_with_clarification('¿Qué sabes hacer?')
    
    print(f"Necesita clarificación: {result.get('needs_clarification', False)}")
    
    if result.get('clarifying_questions'):
        print("Preguntas de aclaración:")
        for i, q in enumerate(result['clarifying_questions'], 1):
            print(f"  {i}. {q}")
    else:
        print("✅ Consulta procesada directamente")
        print(f"Respuesta: {result.get('response', 'N/A')[:200]}...")

def test_multi_query():
    """Test de búsqueda multi-query"""
    print("\n🔍 Probando búsqueda multi-query...")
    
    orchestrator = CVOrchestrator()
    
    queries = [
        "experiencia técnica",
        "proyectos desarrollados",
        "competencias principales"
    ]
    
    result = orchestrator.multi_query_search(queries)
    
    print(f"Éxito: {result['success']}")
    print(f"Resultados encontrados: {result.get('total_found', 0)}")
    print(f"Consultas usadas: {len(result.get('queries_used', []))}")

if __name__ == "__main__":
    test_clarification()
    test_multi_query()