#!/usr/bin/env python3
"""
Demo de Patrones Agentic Implementados

Demostración práctica de las capacidades agentic del CV Agent,
incluyendo Clarifier Agent, Multi-Query Search, y Email Handoff.
"""

import os
import sys
from dotenv import load_dotenv

# Agregar directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.orchestrator import CVOrchestrator
from agent.clarifier import ClarifierAgent
from agent.email_agent import EmailAgent

load_dotenv()

def demo_clarifier_agent():
    """Demostrar funcionalidad del Clarifier Agent"""
    print("\n" + "="*60)
    print("🤔 DEMO: CLARIFIER AGENT")
    print("="*60)
    
    clarifier = ClarifierAgent()
    
    # Consultas ambiguas para probar
    ambiguous_queries = [
        "Cuéntame sobre tus proyectos",
        "¿Qué sabes hacer?",
        "Háblame de tu experiencia",
        "¿Cuál es tu stack tecnológico?"
    ]
    
    for query in ambiguous_queries:
        print(f"\n📝 Consulta ambigua: '{query}'")
        
        try:
            questions = clarifier.generate_clarifying_questions(query)
            
            if questions:
                print("🔍 Preguntas de aclaración generadas:")
                for i, question in enumerate(questions, 1):
                    print(f"   {i}. {question}")
            else:
                print("✅ La consulta es suficientemente clara")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 40)

def demo_multi_query_search():
    """Demostrar búsqueda multi-query"""
    print("\n" + "="*60)
    print("🔍 DEMO: MULTI-QUERY SEARCH")
    print("="*60)
    
    try:
        orchestrator = CVOrchestrator()
        
        # Consultas refinadas relacionadas
        refined_queries = [
            "experiencia en arquitectura de software",
            "proyectos de microservicios",
            "liderazgo técnico en desarrollo",
            "sistemas distribuidos y escalabilidad"
        ]
        
        print(f"🎯 Ejecutando búsqueda con {len(refined_queries)} consultas refinadas:")
        for query in refined_queries:
            print(f"   • {query}")
        
        results = orchestrator.multi_query_search(
            queries=refined_queries,
            document_types=["cv", "projects"]
        )
        
        if results["success"]:
            print(f"\n✅ Encontrados {results['total_found']} resultados únicos")
            print("\n📄 Primeros resultados:")
            
            for i, result in enumerate(results["results"][:3], 1):
                source = result.metadata.get("source", "Desconocido")
                score = result.score
                preview = result.content[:100] + "..." if len(result.content) > 100 else result.content
                
                print(f"\n{i}. Fuente: {source} (Score: {score:.3f})")
                print(f"   Contenido: {preview}")
        else:
            print(f"❌ Error en búsqueda: {results.get('error', 'Desconocido')}")
            
    except Exception as e:
        print(f"❌ Error inicializando orchestrator: {e}")

def demo_query_with_clarification():
    """Demostrar procesamiento con clarificación automática"""
    print("\n" + "="*60)
    print("🔄 DEMO: QUERY WITH CLARIFICATION")
    print("="*60)
    
    try:
        orchestrator = CVOrchestrator()
        
        # Consulta que probablemente necesite clarificación
        ambiguous_query = "¿Qué has hecho últimamente?"
        
        print(f"📝 Consulta ambigua: '{ambiguous_query}'")
        
        result = orchestrator.process_query_with_clarification(
            query=ambiguous_query,
            session_id="demo_session",
            enable_clarification=True
        )
        
        if result.get("needs_clarification", False):
            print("🤔 Se necesita clarificación:")
            questions = result.get("clarifying_questions", [])
            for i, question in enumerate(questions, 1):
                print(f"   {i}. {question}")
                
            print(f"\n💡 Sugerencia: {result.get('suggested_action', 'N/A')}")
        else:
            print("✅ Consulta procesada directamente:")
            print(f"   Respuesta: {result.get('response', 'N/A')[:150]}...")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_email_handoff():
    """Demostrar handoff al Email Agent"""
    print("\n" + "="*60)
    print("📧 DEMO: EMAIL HANDOFF AGENT")
    print("="*60)
    
    email_agent = EmailAgent()
    
    # Datos de prueba
    query = "¿Cuáles son mis principales competencias técnicas?"
    response = """Basado en tu perfil profesional, tus principales competencias técnicas incluyen:

🔧 **Arquitectura y Desarrollo:**
- Arquitectura de microservicios y sistemas distribuidos
- Desarrollo full-stack con Python, Java, y JavaScript
- Patrones de diseño y mejores prácticas de desarrollo

☁️ **Cloud y DevOps:**
- AWS, Azure, y Google Cloud Platform
- Docker, Kubernetes, y orquestación de contenedores
- CI/CD, automatización y monitoreo

📊 **Datos y Analytics:**
- Diseño de pipelines de datos
- Machine Learning y análisis predictivo
- Bases de datos relacionales y NoSQL
"""
    
    recipient = "demo@example.com"  # Email de prueba
    
    print(f"📝 Consulta: {query}")
    print(f"📧 Destinatario: {recipient}")
    print("📤 Intentando enviar resumen por email...")
    
    try:
        result = email_agent.send_query_summary(
            query=query,
            response=response,
            recipient_email=recipient,
            session_id="demo_session"
        )
        
        if result["success"]:
            print("✅ Email enviado exitosamente")
            print(f"   ID del mensaje: {result.get('message_id', 'N/A')}")
        else:
            print(f"❌ Error enviando email: {result.get('error', 'Desconocido')}")
            print("💡 Nota: Esto es normal en modo demo sin configuración SMTP")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Nota: El handoff funciona pero requiere configuración SMTP")

def demo_agents_as_tools():
    """Demostrar patrón Agents-as-Tools"""
    print("\n" + "="*60)
    print("🔧 DEMO: AGENTS-AS-TOOLS PATTERN")
    print("="*60)
    
    try:
        orchestrator = CVOrchestrator()
        
        # Consulta que active múltiples agentes
        complex_query = "Necesito información detallada sobre mi experiencia en cloud computing para una propuesta técnica"
        
        print(f"📝 Consulta compleja: {complex_query}")
        print("\n🔄 Procesando con patrón Agents-as-Tools:")
        
        # 1. Clasificar consulta
        classification = orchestrator.classify_query(complex_query)
        print(f"   1️⃣ Clasificación: {classification.category} ({classification.confidence}%)")
        
        # 2. Determinar si necesita clarificación
        if classification.confidence < 70:
            clarification = orchestrator.generate_clarifying_questions(complex_query)
            if clarification["should_clarify"]:
                print(f"   2️⃣ Clarificación: {len(clarification['questions'])} preguntas generadas")
        
        # 3. Búsqueda multi-query
        search_queries = [
            "experiencia cloud computing AWS Azure",
            "proyectos infraestructura nube",
            "competencias DevOps contenedores"
        ]
        
        search_results = orchestrator.multi_query_search(
            queries=search_queries,
            document_types=["cv", "projects", "clips"]
        )
        
        print(f"   3️⃣ Búsqueda multi-query: {search_results['total_found']} resultados encontrados")
        
        # 4. Generar respuesta final
        final_result = orchestrator.process_query(
            query=complex_query,
            session_id="agents_as_tools_demo"
        )
        
        if final_result["success"]:
            print(f"   4️⃣ Respuesta final generada ({len(final_result['response'])} caracteres)")
            print(f"   ⏱️ Tiempo total: {final_result['metadata']['processing_time']:.2f}s")
            print(f"   🔧 Herramientas usadas: {', '.join(final_result['metadata']['tools_used'])}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Ejecutar todas las demos"""
    print("🚀 DEMO DE PATRONES AGENTIC - CV AGENT")
    print("="*60)
    print("Demostrando capacidades agentic avanzadas implementadas")
    
    # Verificar configuración
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ ADVERTENCIA: OPENAI_API_KEY no configurada")
        print("Algunas demos pueden fallar\n")
    
    try:
        # Ejecutar demos
        demo_clarifier_agent()
        demo_multi_query_search()
        demo_query_with_clarification()
        demo_email_handoff()
        demo_agents_as_tools()
        
        print("\n" + "="*60)
        print("✅ DEMOS COMPLETADAS")
        print("="*60)
        print("Patrones agentic demostrados:")
        print("• Clarifier Agent (3 preguntas de aclaración)")
        print("• Multi-Query Search (fusión de resultados)")
        print("• Query with Clarification (procesamiento inteligente)")
        print("• Email Handoff Agent (delegación especializada)")
        print("• Agents-as-Tools (orquestación compleja)")
        
    except KeyboardInterrupt:
        print("\n👋 Demo interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error general en demo: {e}")

if __name__ == "__main__":
    main()