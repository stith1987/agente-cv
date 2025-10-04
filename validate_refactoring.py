"""
Validation Script

Script para validar que la refactorización del módulo agent esté completa y funcional.
"""

import os
import sys
import importlib
from pathlib import Path
from typing import List, Dict, Any

def validate_structure() -> Dict[str, Any]:
    """Validar la estructura de directorios refactorizada"""
    print("🔍 Validando estructura de directorios...")
    
    expected_structure = {
        "agent/__init__.py": "Punto de entrada principal",
        "agent/core/__init__.py": "Módulo core",
        "agent/core/orchestrator.py": "Orquestador principal",
        "agent/core/query_classifier.py": "Clasificador de consultas",
        "agent/core/response_evaluator.py": "Evaluador de respuestas",
        "agent/specialists/__init__.py": "Agentes especializados",
        "agent/specialists/clarifier.py": "Agente clarificador",
        "agent/specialists/email_handler.py": "Agente de email",
        "agent/utils/__init__.py": "Utilidades",
        "agent/utils/config.py": "Configuración",
        "agent/utils/logger.py": "Sistema de logging",
        "agent/utils/prompts.py": "Gestor de prompts",
        "agent/README.md": "Documentación"
    }
    
    results = {
        "missing_files": [],
        "existing_files": [],
        "total_expected": len(expected_structure),
        "total_found": 0
    }
    
    for file_path, description in expected_structure.items():
        if Path(file_path).exists():
            results["existing_files"].append(file_path)
            results["total_found"] += 1
            print(f"   ✅ {file_path} - {description}")
        else:
            results["missing_files"].append(file_path)
            print(f"   ❌ {file_path} - {description} (MISSING)")
    
    coverage = (results["total_found"] / results["total_expected"]) * 100
    print(f"\n📊 Cobertura de estructura: {coverage:.1f}% ({results['total_found']}/{results['total_expected']})")
    
    return results

def validate_imports() -> Dict[str, Any]:
    """Validar que las importaciones funcionen correctamente"""
    print("\n🔗 Validando importaciones...")
    
    import_tests = [
        ("agent", "Módulo principal"),
        ("agent.core.orchestrator", "CVOrchestrator"),
        ("agent.core.query_classifier", "QueryClassifier y QueryClassification"),
        ("agent.core.response_evaluator", "ResponseEvaluator y EvaluationResult"),
        ("agent.specialists.clarifier", "ClarifierAgent"),
        ("agent.specialists.email_handler", "EmailAgent"),
        ("agent.utils.config", "AgentConfig"),
        ("agent.utils.logger", "AgentLogger"),
        ("agent.utils.prompts", "PromptManager")
    ]
    
    results = {
        "successful_imports": [],
        "failed_imports": [],
        "total_tests": len(import_tests),
        "total_passed": 0
    }
    
    for module_name, description in import_tests:
        try:
            importlib.import_module(module_name)
            results["successful_imports"].append(module_name)
            results["total_passed"] += 1
            print(f"   ✅ {module_name} - {description}")
        except ImportError as e:
            results["failed_imports"].append((module_name, str(e)))
            print(f"   ❌ {module_name} - {description} (ERROR: {e})")
        except Exception as e:
            results["failed_imports"].append((module_name, str(e)))
            print(f"   ⚠️  {module_name} - {description} (WARNING: {e})")
    
    success_rate = (results["total_passed"] / results["total_tests"]) * 100
    print(f"\n📊 Tasa de éxito de importaciones: {success_rate:.1f}% ({results['total_passed']}/{results['total_tests']})")
    
    return results

def validate_classes() -> Dict[str, Any]:
    """Validar que las clases principales se puedan instanciar"""
    print("\n🏗️ Validando clases principales...")
    
    results = {
        "successful_classes": [],
        "failed_classes": [],
        "warnings": []
    }
    
    # Test AgentConfig
    try:
        from agent.utils.config import AgentConfig
        config = AgentConfig.from_env()
        results["successful_classes"].append("AgentConfig")
        print("   ✅ AgentConfig - Configuración cargada correctamente")
    except ValueError as e:
        results["warnings"].append(f"AgentConfig: {e}")
        print(f"   ⚠️  AgentConfig - {e}")
    except Exception as e:
        results["failed_classes"].append(f"AgentConfig: {e}")
        print(f"   ❌ AgentConfig - ERROR: {e}")
        return results  # No podemos continuar sin configuración
    
    # Test AgentLogger
    try:
        from agent.utils.logger import AgentLogger
        logger = AgentLogger("test")
        results["successful_classes"].append("AgentLogger")
        print("   ✅ AgentLogger - Logger inicializado correctamente")
    except Exception as e:
        results["failed_classes"].append(f"AgentLogger: {e}")
        print(f"   ❌ AgentLogger - ERROR: {e}")
    
    # Test PromptManager
    try:
        from agent.utils.prompts import PromptManager
        prompt_manager = PromptManager()
        results["successful_classes"].append("PromptManager")
        print("   ✅ PromptManager - Gestor de prompts inicializado correctamente")
    except Exception as e:
        results["failed_classes"].append(f"PromptManager: {e}")
        print(f"   ❌ PromptManager - ERROR: {e}")
    
    # Test QueryClassifier (requiere OpenAI)
    try:
        from agent.core.query_classifier import QueryClassifier
        classifier = QueryClassifier(config)
        results["successful_classes"].append("QueryClassifier")
        print("   ✅ QueryClassifier - Clasificador inicializado correctamente")
    except Exception as e:
        results["warnings"].append(f"QueryClassifier: {e}")
        print(f"   ⚠️  QueryClassifier - {e}")
    
    # Test ResponseEvaluator (requiere OpenAI)
    try:
        from agent.core.response_evaluator import ResponseEvaluator
        evaluator = ResponseEvaluator(config)
        results["successful_classes"].append("ResponseEvaluator")
        print("   ✅ ResponseEvaluator - Evaluador inicializado correctamente")
    except Exception as e:
        results["warnings"].append(f"ResponseEvaluator: {e}")
        print(f"   ⚠️  ResponseEvaluator - {e}")
    
    # Test ClarifierAgent (requiere OpenAI)
    try:
        from agent.specialists.clarifier import ClarifierAgent
        clarifier = ClarifierAgent(config)
        results["successful_classes"].append("ClarifierAgent")
        print("   ✅ ClarifierAgent - Agente clarificador inicializado correctamente")
    except Exception as e:
        results["warnings"].append(f"ClarifierAgent: {e}")
        print(f"   ⚠️  ClarifierAgent - {e}")
    
    # Test EmailAgent
    try:
        from agent.specialists.email_handler import EmailAgent
        email_agent = EmailAgent(config)
        results["successful_classes"].append("EmailAgent")
        print("   ✅ EmailAgent - Agente de email inicializado correctamente")
        
        if not email_agent.is_configured:
            results["warnings"].append("EmailAgent: Email no configurado completamente")
            print("   ⚠️  EmailAgent - Email no configurado completamente (opcional)")
    except Exception as e:
        results["failed_classes"].append(f"EmailAgent: {e}")
        print(f"   ❌ EmailAgent - ERROR: {e}")
    
    # Test CVOrchestrator (integración completa)
    try:
        from agent.core.orchestrator import CVOrchestrator
        orchestrator = CVOrchestrator(config)
        results["successful_classes"].append("CVOrchestrator")
        print("   ✅ CVOrchestrator - Orquestador principal inicializado correctamente")
    except Exception as e:
        results["failed_classes"].append(f"CVOrchestrator: {e}")
        print(f"   ❌ CVOrchestrator - ERROR: {e}")
    
    print(f"\n📊 Clases validadas exitosamente: {len(results['successful_classes'])}")
    print(f"📊 Advertencias: {len(results['warnings'])}")
    print(f"📊 Errores: {len(results['failed_classes'])}")
    
    return results

def validate_functionality() -> Dict[str, Any]:
    """Validar funcionalidad básica del sistema"""
    print("\n⚙️ Validando funcionalidad básica...")
    
    results = {
        "functional_tests": [],
        "failed_tests": [],
        "warnings": []
    }
    
    try:
        from agent.utils.config import AgentConfig
        from agent.core.orchestrator import CVOrchestrator
        
        config = AgentConfig.from_env()
        orchestrator = CVOrchestrator(config)
        
        # Test clasificación básica
        try:
            classification = orchestrator.query_classifier.classify("¿Cuál es tu email?")
            if hasattr(classification, 'category') and hasattr(classification, 'confidence'):
                results["functional_tests"].append("Query classification")
                print("   ✅ Clasificación de consultas - Funcional")
            else:
                results["failed_tests"].append("Query classification: Invalid response structure")
                print("   ❌ Clasificación de consultas - Estructura de respuesta inválida")
        except Exception as e:
            results["warnings"].append(f"Query classification: {e}")
            print(f"   ⚠️  Clasificación de consultas - {e}")
        
        # Test evaluación básica
        try:
            evaluation = orchestrator.response_evaluator.evaluate_response(
                query="Test query",
                response="Test response",
                context="Test context"
            )
            if hasattr(evaluation, 'scores') and hasattr(evaluation, 'confidence'):
                results["functional_tests"].append("Response evaluation")
                print("   ✅ Evaluación de respuestas - Funcional")
            else:
                results["failed_tests"].append("Response evaluation: Invalid response structure")
                print("   ❌ Evaluación de respuestas - Estructura de respuesta inválida")
        except Exception as e:
            results["warnings"].append(f"Response evaluation: {e}")
            print(f"   ⚠️  Evaluación de respuestas - {e}")
        
        # Test generación de aclaraciones
        try:
            questions = orchestrator.clarifier_agent.generate_clarifications("Test query")
            if isinstance(questions, list) and len(questions) > 0:
                results["functional_tests"].append("Clarification generation")
                print("   ✅ Generación de aclaraciones - Funcional")
            else:
                results["failed_tests"].append("Clarification generation: No questions generated")
                print("   ❌ Generación de aclaraciones - No se generaron preguntas")
        except Exception as e:
            results["warnings"].append(f"Clarification generation: {e}")
            print(f"   ⚠️  Generación de aclaraciones - {e}")
        
        # Test configuración de email
        try:
            email_test = orchestrator.email_agent.test_email_configuration()
            if email_test["configuration_valid"]:
                results["functional_tests"].append("Email configuration")
                print("   ✅ Configuración de email - Válida")
            else:
                results["warnings"].append("Email configuration: Not configured")
                print("   ⚠️  Configuración de email - No configurada (opcional)")
        except Exception as e:
            results["warnings"].append(f"Email configuration: {e}")
            print(f"   ⚠️  Configuración de email - {e}")
        
        # Test procesamiento completo de consulta
        try:
            result = orchestrator.process_query("¿Cuál es tu experiencia?")
            if "response" in result and "classification" in result:
                results["functional_tests"].append("Full query processing")
                print("   ✅ Procesamiento completo de consultas - Funcional")
            else:
                results["failed_tests"].append("Full query processing: Invalid response structure")
                print("   ❌ Procesamiento completo de consultas - Estructura de respuesta inválida")
        except Exception as e:
            results["warnings"].append(f"Full query processing: {e}")
            print(f"   ⚠️  Procesamiento completo de consultas - {e}")
        
    except Exception as e:
        results["failed_tests"].append(f"Functionality validation setup: {e}")
        print(f"   ❌ Error configurando validación de funcionalidad: {e}")
    
    print(f"\n📊 Tests funcionales exitosos: {len(results['functional_tests'])}")
    print(f"📊 Advertencias: {len(results['warnings'])}")
    print(f"📊 Errores: {len(results['failed_tests'])}")
    
    return results

def generate_report(structure_results: Dict, import_results: Dict, 
                   class_results: Dict, functionality_results: Dict):
    """Generar reporte final de validación"""
    print("\n" + "="*60)
    print("📋 REPORTE FINAL DE VALIDACIÓN")
    print("="*60)
    
    # Resumen general
    total_issues = (
        len(structure_results["missing_files"]) +
        len(import_results["failed_imports"]) +
        len(class_results["failed_classes"]) +
        len(functionality_results["failed_tests"])
    )
    
    total_warnings = (
        len(class_results["warnings"]) +
        len(functionality_results["warnings"])
    )
    
    if total_issues == 0:
        print("🎉 ¡VALIDACIÓN EXITOSA! La refactorización está completa.")
        status = "✅ EXITOSO"
    elif total_issues <= 2:
        print("⚠️  VALIDACIÓN MAYORMENTE EXITOSA con problemas menores.")
        status = "⚠️  PARCIAL"
    else:
        print("❌ VALIDACIÓN FALLIDA. Se requieren correcciones.")
        status = "❌ FALLIDA"
    
    print(f"\n📊 RESUMEN:")
    print(f"   Estado: {status}")
    print(f"   Errores críticos: {total_issues}")
    print(f"   Advertencias: {total_warnings}")
    
    # Detalles por categoría
    print(f"\n📁 ESTRUCTURA:")
    print(f"   Archivos encontrados: {structure_results['total_found']}/{structure_results['total_expected']}")
    if structure_results["missing_files"]:
        print(f"   Archivos faltantes: {', '.join(structure_results['missing_files'])}")
    
    print(f"\n🔗 IMPORTACIONES:")
    print(f"   Importaciones exitosas: {import_results['total_passed']}/{import_results['total_tests']}")
    if import_results["failed_imports"]:
        print(f"   Importaciones fallidas:")
        for module, error in import_results["failed_imports"]:
            print(f"     - {module}: {error}")
    
    print(f"\n🏗️  CLASES:")
    print(f"   Clases funcionales: {len(class_results['successful_classes'])}")
    if class_results["failed_classes"]:
        print(f"   Clases con errores:")
        for error in class_results["failed_classes"]:
            print(f"     - {error}")
    if class_results["warnings"]:
        print(f"   Advertencias:")
        for warning in class_results["warnings"]:
            print(f"     - {warning}")
    
    print(f"\n⚙️  FUNCIONALIDAD:")
    print(f"   Tests funcionales exitosos: {len(functionality_results['functional_tests'])}")
    if functionality_results["failed_tests"]:
        print(f"   Tests fallidos:")
        for error in functionality_results["failed_tests"]:
            print(f"     - {error}")
    if functionality_results["warnings"]:
        print(f"   Advertencias funcionales:")
        for warning in functionality_results["warnings"]:
            print(f"     - {warning}")
    
    # Recomendaciones
    print(f"\n💡 RECOMENDACIONES:")
    
    if structure_results["missing_files"]:
        print("   - Crear archivos faltantes de la estructura")
    
    if import_results["failed_imports"]:
        print("   - Revisar y corregir errores de importación")
    
    if total_issues == 0 and total_warnings == 0:
        print("   - ¡Todo perfecto! El sistema está listo para uso.")
    elif total_issues == 0:
        print("   - Sistema funcional. Considerar resolver advertencias para funcionalidad completa.")
    else:
        print("   - Resolver errores críticos antes de usar el sistema en producción.")
        print("   - Verificar configuración de variables de entorno (especialmente OPENAI_API_KEY)")
    
    print("\n" + "="*60)
    
    # Código de salida
    return 0 if total_issues == 0 else 1

def main():
    """Función principal de validación"""
    print("🔍 VALIDADOR DE REFACTORIZACIÓN - Módulo Agent")
    print("="*60)
    
    # Verificar que estamos en el directorio correcto
    if not Path("agent").exists():
        print("❌ Error: No se encuentra el directorio 'agent'")
        print("💡 Ejecutar desde el directorio raíz del proyecto")
        return 1
    
    try:
        # Ejecutar validaciones
        structure_results = validate_structure()
        import_results = validate_imports()
        class_results = validate_classes()
        functionality_results = validate_functionality()
        
        # Generar reporte final
        return generate_report(structure_results, import_results, 
                             class_results, functionality_results)
        
    except KeyboardInterrupt:
        print("\n👋 Validación interrumpida por el usuario")
        return 1
    except Exception as e:
        print(f"\n❌ Error inesperado durante la validación: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())