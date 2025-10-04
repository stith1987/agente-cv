"""
Ejemplo de Uso - Agente CV Refactorizado

Demuestra el uso de la nueva arquitectura refactorizada del módulo agent.
"""

import asyncio
from typing import Dict, Any

# Importaciones de la nueva estructura
from agent import CVOrchestrator
from agent.utils.config import AgentConfig
from agent.utils.logger import AgentLogger
from agent.core.query_classifier import QueryCategory, RecommendedTool


async def demo_refactored_agent():
    """Demostración del agente refactorizado"""
    
    print("🚀 Demo: Agente CV Refactorizado")
    print("=" * 50)
    
    # 1. Configuración
    print("\n1️⃣ Inicializando configuración...")
    try:
        config = AgentConfig.from_env()
        print(f"   ✅ Configuración cargada: {config.openai.model}")
        print(f"   📧 Email configurado: {config.email.is_configured()}")
    except Exception as e:
        print(f"   ❌ Error en configuración: {e}")
        return
    
    # 2. Inicializar orquestador
    print("\n2️⃣ Inicializando orquestador...")
    try:
        orchestrator = CVOrchestrator(config)
        print("   ✅ Orquestador inicializado exitosamente")
    except Exception as e:
        print(f"   ❌ Error inicializando orquestador: {e}")
        return
    
    # 3. Consultas de ejemplo
    example_queries = [
        "¿Cuál es tu experiencia en microservicios?",
        "¿Qué proyectos has desarrollado en fintech?", 
        "¿Cuál es tu email de contacto?",
        "Háblame sobre tu experiencia general",
        "¿Qué tecnologías dominas?"
    ]
    
    print(f"\n3️⃣ Procesando {len(example_queries)} consultas de ejemplo...")
    
    for i, query in enumerate(example_queries, 1):
        print(f"\n--- Consulta {i}: {query} ---")
        
        try:
            # Procesar consulta
            result = orchestrator.process_query(
                query=query,
                context={"session_id": "demo", "user_preferences": {"detail_level": 3}}
            )
            
            # Mostrar resultados
            classification = result.get("classification", {})
            evaluation = result.get("evaluation", {})
            
            print(f"📊 Clasificación:")
            print(f"   Categoría: {classification.get('category', 'N/A')}")
            print(f"   Tool recomendado: {classification.get('recommended_tool', 'N/A')}")
            print(f"   Confianza: {classification.get('confidence', 0):.1f}%")
            
            print(f"📈 Evaluación:")
            print(f"   Puntuación: {evaluation.get('overall_score', 0):.1f}/10")
            print(f"   ¿Alta calidad?: {'✅' if evaluation.get('overall_score', 0) >= 7.0 else '❌'}")
            
            print(f"🔧 Metadata:")
            metadata = result.get("metadata", {})
            print(f"   Fuente: {result.get('source', 'N/A')}")
            print(f"   Herramientas: {metadata.get('tools_used', [])}")
            
            response = result.get("response", "")
            print(f"💬 Respuesta: {response[:100]}{'...' if len(response) > 100 else ''}")
            
            # Manejar preguntas de aclaración
            if "clarification_questions" in result:
                print("❓ Preguntas de aclaración:")
                for j, question in enumerate(result["clarification_questions"], 1):
                    print(f"   {j}. {question}")
        
        except Exception as e:
            print(f"   ❌ Error procesando consulta: {e}")
    
    # 4. Estadísticas finales
    print(f"\n4️⃣ Estadísticas finales:")
    
    try:
        stats = orchestrator.get_session_stats()
        
        print(f"📊 Sesión:")
        print(f"   Total consultas: {stats['total_queries']}")
        print(f"   Exitosas: {stats['successful_queries']}")
        print(f"   Tiempo promedio: {stats['average_response_time']:.2f}s")
        
        print(f"🔍 Clasificador:")
        classifier_stats = stats.get('classifier_stats', {})
        print(f"   Tasa de éxito: {classifier_stats.get('success_rate', 0):.1f}%")
        
        print(f"📈 Evaluador:")
        evaluator_stats = stats.get('evaluator_stats', {})
        print(f"   Puntuación promedio: {evaluator_stats.get('average_score', 0):.1f}/10")
        print(f"   Respuestas de calidad: {evaluator_stats.get('quality_rate', 0):.1f}%")
        
    except Exception as e:
        print(f"   ❌ Error obteniendo estadísticas: {e}")
    
    # 5. Demostración de componentes individuales
    print(f"\n5️⃣ Demo componentes individuales:")
    
    # Clasificador
    print("\n🔍 Clasificador de consultas:")
    try:
        test_query = "¿Qué experiencia tienes trabajando con APIs?"
        classification = orchestrator.query_classifier.classify(test_query)
        
        print(f"   Query: {test_query}")
        print(f"   Categoría: {classification.category.value}")
        print(f"   Tool: {classification.recommended_tool.value}")
        print(f"   Términos de búsqueda: {classification.search_terms}")
        print(f"   ¿Necesita aclaración?: {classification.needs_clarification()}")
        
    except Exception as e:
        print(f"   ❌ Error en clasificador: {e}")
    
    # Evaluador
    print("\n📈 Evaluador de respuestas:")
    try:
        test_response = "Tengo amplia experiencia desarrollando APIs RESTful con Spring Boot, incluyendo autenticación JWT, documentación con Swagger y testing automatizado."
        evaluation = orchestrator.response_evaluator.evaluate_response(
            query="¿Qué experiencia tienes con APIs?",
            response=test_response,
            context="Información técnica específica del CV"
        )
        
        print(f"   Puntuación general: {evaluation.scores.overall_score:.1f}/10")
        print(f"   Precisión: {evaluation.scores.precision:.1f}/10")
        print(f"   Completitud: {evaluation.scores.completeness:.1f}/10")
        print(f"   Relevancia: {evaluation.scores.relevance:.1f}/10")
        print(f"   Fortalezas: {', '.join(evaluation.strengths[:2])}")
        
    except Exception as e:
        print(f"   ❌ Error en evaluador: {e}")
    
    # Generador de aclaraciones
    print("\n❓ Generador de aclaraciones:")
    try:
        vague_query = "Información sobre proyectos"
        questions = orchestrator.clarifier_agent.generate_clarifications(vague_query)
        
        print(f"   Query vaga: {vague_query}")
        print(f"   Preguntas generadas:")
        for i, question in enumerate(questions, 1):
            print(f"     {i}. {question}")
            
    except Exception as e:
        print(f"   ❌ Error en generador de aclaraciones: {e}")
    
    # 6. Test de email (si está configurado)
    if config.email.is_configured():
        print(f"\n📧 Test de configuración de email:")
        try:
            test_result = orchestrator.email_agent.test_email_configuration()
            print(f"   Configuración válida: {'✅' if test_result['configuration_valid'] else '❌'}")
            print(f"   Conexión exitosa: {'✅' if test_result['connection_successful'] else '❌'}")
            for detail in test_result['details']:
                print(f"   - {detail}")
                
        except Exception as e:
            print(f"   ❌ Error en test de email: {e}")
    else:
        print(f"\n📧 Email no configurado (opcional)")
    
    print(f"\n🎉 Demo completada exitosamente!")
    print("=" * 50)


async def demo_advanced_features():
    """Demostración de características avanzadas"""
    
    print("\n🔬 Demo: Características Avanzadas")
    print("=" * 40)
    
    try:
        config = AgentConfig.from_env()
        orchestrator = CVOrchestrator(config)
        
        # Análisis de necesidad de aclaración
        print("\n1️⃣ Análisis de necesidad de aclaración:")
        
        queries_to_analyze = [
            "¿Qué?",  # Muy vaga
            "Información",  # Muy vaga
            "¿Qué experiencia tienes en desarrollo de APIs RESTful con Spring Boot?",  # Específica
            "Háblame de proyectos y tecnologías y experiencia"  # Múltiples temas
        ]
        
        for query in queries_to_analyze:
            analysis = orchestrator.clarifier_agent.analyze_clarification_need(query)
            print(f"   '{query}'")
            print(f"   → Necesita aclaración: {'✅' if analysis['needs_clarification'] else '❌'}")
            print(f"   → Confianza: {analysis['confidence']}%")
            print(f"   → Urgencia: {analysis['urgency']}")
            if analysis['reasons']:
                print(f"   → Razones: {', '.join(analysis['reasons'])}")
            print()
        
        # Auto-crítica del sistema
        print("2️⃣ Auto-crítica del sistema:")
        
        test_query = "¿Qué proyectos de fintech has desarrollado?"
        result = orchestrator.process_query(test_query)
        
        critique = orchestrator.response_evaluator.self_critique(
            query=test_query,
            response=result.get("response", ""),
            tools_used=result.get("metadata", {}).get("tools_used", []),
            context_quality="high"
        )
        
        print(f"   Query: {test_query}")
        print(f"   Éxito: {'✅' if critique['success'] else '❌'}")
        print(f"   Crítica: {critique['critique']}")
        print(f"   Puntuación: {critique.get('overall_score', 'N/A')}")
        
        insights = critique.get('insights', {})
        if insights:
            print(f"   Insights:")
            for key, value in insights.items():
                print(f"     - {key}: {value}")
        
        recommendations = critique.get('recommendations', [])
        if recommendations:
            print(f"   Recomendaciones:")
            for rec in recommendations:
                print(f"     - {rec}")
        
    except Exception as e:
        print(f"❌ Error en demo avanzada: {e}")


def main():
    """Función principal"""
    print("🤖 Sistema de Agente CV - Demo Refactorizado")
    print("=" * 60)
    
    # Verificar configuración básica
    try:
        config = AgentConfig.from_env()
        print("✅ Configuración básica verificada")
    except Exception as e:
        print(f"❌ Error de configuración: {e}")
        print("💡 Asegúrate de tener configurada la variable OPENAI_API_KEY")
        return
    
    # Ejecutar demos
    try:
        # Demo principal
        asyncio.run(demo_refactored_agent())
        
        # Demo avanzada
        asyncio.run(demo_advanced_features())
        
        print("\n🎯 Próximos pasos:")
        print("1. Revisar logs generados en 'logs/agent.log'")
        print("2. Configurar email para funcionalidad completa")
        print("3. Personalizar configuración según necesidades")
        print("4. Integrar con el resto de la aplicación")
        
    except KeyboardInterrupt:
        print("\n👋 Demo interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()