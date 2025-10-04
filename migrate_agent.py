"""
Migration Script

Script para migrar el código existente a la nueva estructura refactorizada.
"""

import os
import re
from pathlib import Path

# Mapeo de importaciones antiguas a nuevas
IMPORT_MAPPINGS = {
    # Orquestador principal
    "from agent.orchestrator import CVOrchestrator": "from agent.core.orchestrator import CVOrchestrator",
    "from agent.orchestrator import QueryClassification": "from agent.core.query_classifier import QueryClassification",
    
    # Agentes especializados
    "from agent.clarifier import ClarifierAgent": "from agent.specialists.clarifier import ClarifierAgent",
    "from agent.email_agent import EmailAgent": "from agent.specialists.email_handler import EmailAgent",
    
    # Evaluador
    "from agent.evaluator import ResponseEvaluator": "from agent.core.response_evaluator import ResponseEvaluator",
    "from agent.evaluator import EvaluationResult": "from agent.core.response_evaluator import EvaluationResult",
    
    # Prompts
    "from agent.prompts import": "from agent.utils.prompts import PromptManager",
    "format_system_prompt": "PromptManager().format_system_prompt",
    "format_classification_prompt": "PromptManager().format_classification_prompt",
    "format_evaluation_prompt": "PromptManager().format_evaluation_prompt",
    "format_error_response": "PromptManager().format_error_response",
}

def migrate_file(file_path: Path) -> bool:
    """
    Migrar un archivo a la nueva estructura
    
    Args:
        file_path: Ruta del archivo a migrar
        
    Returns:
        True si se realizaron cambios
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = False
        
        # Aplicar mapeos de importaciones
        for old_import, new_import in IMPORT_MAPPINGS.items():
            if old_import in content:
                content = content.replace(old_import, new_import)
                changes_made = True
                print(f"  ✓ Updated import: {old_import} -> {new_import}")
        
        # Actualizar instanciaciones específicas
        if "CVOrchestrator()" in content:
            # Agregar configuración por defecto
            content = content.replace(
                "CVOrchestrator()",
                "CVOrchestrator(AgentConfig.from_env())"
            )
            changes_made = True
            print("  ✓ Updated CVOrchestrator instantiation")
        
        # Guardar cambios si se hicieron
        if changes_made:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Migrated: {file_path.relative_to(Path.cwd())}")
            return True
        
        return False
        
    except Exception as e:
        print(f"✗ Error migrating {file_path}: {e}")
        return False

def migrate_project():
    """Migrar todo el proyecto a la nueva estructura"""
    print("🔄 Starting project migration to refactored agent structure...")
    
    # Directorios a migrar (excluir agent/ ya que fue refactorizado)
    directories_to_check = [
        "api/",
        "rag/",
        "tools/",
        "examples/",
        ".",  # Archivos raíz
    ]
    
    total_files = 0
    migrated_files = 0
    
    for directory in directories_to_check:
        dir_path = Path(directory)
        if not dir_path.exists():
            continue
            
        # Buscar archivos Python
        pattern = "*.py" if directory != "." else "*.py"
        
        for file_path in dir_path.glob(pattern):
            # Excluir ciertos archivos
            if (file_path.name.startswith('.') or 
                file_path.name == '__pycache__' or
                'agent/' in str(file_path)):
                continue
            
            total_files += 1
            print(f"\n📄 Checking {file_path.relative_to(Path.cwd())}...")
            
            if migrate_file(file_path):
                migrated_files += 1
    
    print(f"\n✅ Migration completed!")
    print(f"   Total files checked: {total_files}")
    print(f"   Files migrated: {migrated_files}")
    
    # Crear archivo de compatibilidad temporal
    create_compatibility_layer()

def create_compatibility_layer():
    """Crear capa de compatibilidad para importaciones antiguas"""
    print("\n🔧 Creating compatibility layer...")
    
    # Crear archivo de compatibilidad en agent/
    compatibility_content = '''"""
Compatibility Layer

Mantiene compatibilidad con importaciones antiguas durante la transición.
¡DEPRECADO! Usar las nuevas importaciones directamente.
"""

import warnings

# Importaciones de compatibilidad
from .core.orchestrator import CVOrchestrator
from .core.query_classifier import QueryClassification, QueryClassifier
from .core.response_evaluator import ResponseEvaluator, EvaluationResult
from .specialists.clarifier import ClarifierAgent
from .specialists.email_handler import EmailAgent
from .utils.prompts import PromptManager

# Funciones de prompts deprecadas
def format_system_prompt(*args, **kwargs):
    warnings.warn("format_system_prompt is deprecated. Use PromptManager().format_system_prompt()", 
                  DeprecationWarning, stacklevel=2)
    return PromptManager().format_system_prompt(*args, **kwargs)

def format_classification_prompt(*args, **kwargs):
    warnings.warn("format_classification_prompt is deprecated. Use PromptManager().format_classification_prompt()", 
                  DeprecationWarning, stacklevel=2)
    return PromptManager().format_classification_prompt(*args, **kwargs)

def format_evaluation_prompt(*args, **kwargs):
    warnings.warn("format_evaluation_prompt is deprecated. Use PromptManager().format_evaluation_prompt()", 
                  DeprecationWarning, stacklevel=2)
    return PromptManager().format_evaluation_prompt(*args, **kwargs)

def format_error_response(*args, **kwargs):
    warnings.warn("format_error_response is deprecated. Use PromptManager().format_error_response()", 
                  DeprecationWarning, stacklevel=2)
    return PromptManager().format_error_response(*args, **kwargs)

# Exportaciones para compatibilidad
__all__ = [
    "CVOrchestrator",
    "QueryClassification", 
    "QueryClassifier",
    "ResponseEvaluator",
    "EvaluationResult",
    "ClarifierAgent", 
    "EmailAgent",
    "PromptManager",
    "format_system_prompt",
    "format_classification_prompt", 
    "format_evaluation_prompt",
    "format_error_response"
]
'''
    
    # Escribir archivo de compatibilidad (respaldando el anterior)
    old_file = Path("agent/orchestrator.py")
    if old_file.exists():
        backup_file = Path("agent/orchestrator.py.backup")
        old_file.rename(backup_file)
        print(f"  📦 Backed up old orchestrator to {backup_file}")
    
    # No sobrescribimos el __init__.py principal, solo lo extendemos si es necesario
    print("  ✅ Compatibility layer ready")

if __name__ == "__main__":
    migrate_project()