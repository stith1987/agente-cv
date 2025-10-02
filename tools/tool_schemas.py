"""
Tool Schemas

JSON schemas para tool calling con LLMs. Define las estructuras de datos
y validaciones para las herramientas disponibles en el agente.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class ToolType(str, Enum):
    """Tipos de herramientas disponibles"""
    RAG_SEARCH = "rag_search"
    FAQ_QUERY = "faq_query"
    NOTIFICATION = "notification"
    COMBINED_SEARCH = "combined_search"

class Priority(str, Enum):
    """Niveles de prioridad para notificaciones"""
    LOW = "low"      # -1
    NORMAL = "normal" # 0
    HIGH = "high"    # 1
    EMERGENCY = "emergency"  # 2

# ==================== RAG Search Tool ====================

class RAGSearchParams(BaseModel):
    """Parámetros para búsqueda RAG"""
    query: str = Field(
        description="Consulta de búsqueda semántica",
        min_length=3,
        max_length=500
    )
    document_type: Optional[str] = Field(
        default=None,
        description="Filtrar por tipo de documento: 'cv', 'project', 'clip', 'general'"
    )
    top_k: Optional[int] = Field(
        default=5,
        ge=1,
        le=20,
        description="Número máximo de resultados a retornar"
    )
    similarity_threshold: Optional[float] = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Umbral mínimo de similitud"
    )

class RAGSearchResult(BaseModel):
    """Resultado de búsqueda RAG"""
    content: str = Field(description="Contenido del documento encontrado")
    metadata: Dict[str, Any] = Field(description="Metadatos del documento")
    score: float = Field(description="Score de similitud")
    chunk_id: str = Field(description="ID único del chunk")

class RAGSearchResponse(BaseModel):
    """Respuesta completa de búsqueda RAG"""
    results: List[RAGSearchResult] = Field(description="Lista de resultados")
    total_found: int = Field(description="Total de resultados encontrados")
    query_processed: str = Field(description="Query procesada")
    search_metadata: Dict[str, Any] = Field(
        description="Metadatos de la búsqueda",
        default_factory=dict
    )

# ==================== FAQ Query Tool ====================

class FAQQueryParams(BaseModel):
    """Parámetros para consulta FAQ"""
    query: str = Field(
        description="Consulta para buscar en FAQs",
        min_length=3,
        max_length=200
    )
    category: Optional[str] = Field(
        default=None,
        description="Categoría específica de FAQ"
    )
    limit: Optional[int] = Field(
        default=5,
        ge=1,
        le=10,
        description="Número máximo de FAQs a retornar"
    )
    min_confidence: Optional[float] = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="Confianza mínima requerida"
    )

class FAQResult(BaseModel):
    """Resultado individual de FAQ"""
    question: str = Field(description="Pregunta frecuente")
    answer: str = Field(description="Respuesta a la pregunta")
    category: str = Field(description="Categoría de la FAQ")
    tags: List[str] = Field(description="Tags asociados")
    confidence: float = Field(description="Nivel de confianza de la coincidencia")

class FAQQueryResponse(BaseModel):
    """Respuesta completa de consulta FAQ"""
    results: List[FAQResult] = Field(description="Lista de FAQs encontradas")
    total_found: int = Field(description="Total de FAQs encontradas")
    categories_searched: List[str] = Field(description="Categorías consultadas")
    query_processed: str = Field(description="Query procesada")

# ==================== Notification Tool ====================

class NotificationParams(BaseModel):
    """Parámetros para enviar notificación"""
    message: str = Field(
        description="Mensaje de la notificación",
        min_length=1,
        max_length=1024
    )
    title: Optional[str] = Field(
        default="CV Agent",
        max_length=250,
        description="Título de la notificación"
    )
    priority: Optional[Priority] = Field(
        default=Priority.NORMAL,
        description="Prioridad de la notificación"
    )
    sound: Optional[str] = Field(
        default="default",
        description="Sonido de la notificación"
    )
    url: Optional[str] = Field(
        default=None,
        description="URL opcional para incluir"
    )
    url_title: Optional[str] = Field(
        default=None,
        description="Título del URL"
    )

class NotificationResponse(BaseModel):
    """Respuesta de envío de notificación"""
    success: bool = Field(description="Si la notificación fue enviada exitosamente")
    message: str = Field(description="Mensaje de estado")
    request_id: Optional[str] = Field(description="ID de solicitud de la notificación")
    timestamp: str = Field(description="Timestamp del envío")

# ==================== Combined Search Tool ====================

class CombinedSearchParams(BaseModel):
    """Parámetros para búsqueda combinada RAG + FAQ"""
    query: str = Field(
        description="Consulta para búsqueda combinada",
        min_length=3,
        max_length=500
    )
    include_rag: Optional[bool] = Field(
        default=True,
        description="Incluir búsqueda RAG"
    )
    include_faq: Optional[bool] = Field(
        default=True,
        description="Incluir búsqueda FAQ"
    )
    rag_params: Optional[RAGSearchParams] = Field(
        default=None,
        description="Parámetros específicos para RAG"
    )
    faq_params: Optional[FAQQueryParams] = Field(
        default=None,
        description="Parámetros específicos para FAQ"
    )
    merge_strategy: Optional[str] = Field(
        default="relevance",
        description="Estrategia para combinar resultados: 'relevance', 'type', 'balanced'"
    )

class CombinedSearchResponse(BaseModel):
    """Respuesta de búsqueda combinada"""
    rag_results: Optional[RAGSearchResponse] = Field(description="Resultados RAG")
    faq_results: Optional[FAQQueryResponse] = Field(description="Resultados FAQ")
    combined_summary: str = Field(description="Resumen combinado de resultados")
    total_sources: int = Field(description="Total de fuentes consultadas")
    search_strategy: str = Field(description="Estrategia de búsqueda utilizada")

# ==================== Tool Registry ====================

class ToolDefinition(BaseModel):
    """Definición de una herramienta"""
    name: str = Field(description="Nombre de la herramienta")
    description: str = Field(description="Descripción de la herramienta")
    tool_type: ToolType = Field(description="Tipo de herramienta")
    parameters_schema: Dict[str, Any] = Field(description="Schema JSON de parámetros")
    response_schema: Dict[str, Any] = Field(description="Schema JSON de respuesta")
    examples: List[Dict[str, Any]] = Field(
        description="Ejemplos de uso",
        default_factory=list
    )

# ==================== Tool Schemas Registry ====================

def get_rag_search_tool_schema() -> Dict[str, Any]:
    """Schema para herramienta de búsqueda RAG"""
    return {
        "type": "function",
        "function": {
            "name": "rag_search",
            "description": "Realizar búsqueda semántica en documentos del CV y proyectos usando RAG",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Consulta de búsqueda semántica",
                        "minLength": 3,
                        "maxLength": 500
                    },
                    "document_type": {
                        "type": "string",
                        "enum": ["cv", "project", "clip", "general"],
                        "description": "Filtrar por tipo de documento específico"
                    },
                    "top_k": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 20,
                        "default": 5,
                        "description": "Número máximo de resultados"
                    },
                    "similarity_threshold": {
                        "type": "number",
                        "minimum": 0.0,
                        "maximum": 1.0,
                        "default": 0.7,
                        "description": "Umbral mínimo de similitud"
                    }
                },
                "required": ["query"]
            }
        }
    }

def get_faq_query_tool_schema() -> Dict[str, Any]:
    """Schema para herramienta de consulta FAQ"""
    return {
        "type": "function",
        "function": {
            "name": "faq_query",
            "description": "Consultar base de datos de preguntas frecuentes sobre el CV",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Consulta para buscar en FAQs",
                        "minLength": 3,
                        "maxLength": 200
                    },
                    "category": {
                        "type": "string",
                        "enum": [
                            "tecnologias", "experiencia", "industria", 
                            "certificaciones", "educacion", "proyectos",
                            "metodologias", "publicaciones", "idiomas", 
                            "fortalezas", "general"
                        ],
                        "description": "Categoría específica de FAQ"
                    },
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 10,
                        "default": 5,
                        "description": "Número máximo de FAQs a retornar"
                    },
                    "min_confidence": {
                        "type": "number",
                        "minimum": 0.0,
                        "maximum": 1.0,
                        "default": 0.3,
                        "description": "Confianza mínima requerida"
                    }
                },
                "required": ["query"]
            }
        }
    }

def get_notification_tool_schema() -> Dict[str, Any]:
    """Schema para herramienta de notificaciones"""
    return {
        "type": "function",
        "function": {
            "name": "send_notification",
            "description": "Enviar notificación push sobre consultas o eventos importantes",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Mensaje de la notificación",
                        "minLength": 1,
                        "maxLength": 1024
                    },
                    "title": {
                        "type": "string",
                        "default": "CV Agent",
                        "maxLength": 250,
                        "description": "Título de la notificación"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "normal", "high", "emergency"],
                        "default": "normal",
                        "description": "Prioridad de la notificación"
                    },
                    "sound": {
                        "type": "string",
                        "default": "default",
                        "description": "Sonido de la notificación"
                    },
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "description": "URL opcional para incluir"
                    },
                    "url_title": {
                        "type": "string",
                        "description": "Título del URL"
                    }
                },
                "required": ["message"]
            }
        }
    }

def get_combined_search_tool_schema() -> Dict[str, Any]:
    """Schema para herramienta de búsqueda combinada"""
    return {
        "type": "function",
        "function": {
            "name": "combined_search",
            "description": "Realizar búsqueda combinada en RAG y FAQ para obtener respuesta completa",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Consulta para búsqueda combinada",
                        "minLength": 3,
                        "maxLength": 500
                    },
                    "include_rag": {
                        "type": "boolean",
                        "default": True,
                        "description": "Incluir búsqueda RAG"
                    },
                    "include_faq": {
                        "type": "boolean",
                        "default": True,
                        "description": "Incluir búsqueda FAQ"
                    },
                    "merge_strategy": {
                        "type": "string",
                        "enum": ["relevance", "type", "balanced"],
                        "default": "relevance",
                        "description": "Estrategia para combinar resultados"
                    }
                },
                "required": ["query"]
            }
        }
    }

def get_all_tool_schemas() -> List[Dict[str, Any]]:
    """Obtener todos los schemas de herramientas disponibles"""
    return [
        get_rag_search_tool_schema(),
        get_faq_query_tool_schema(),
        get_notification_tool_schema(),
        get_combined_search_tool_schema()
    ]

def get_tool_registry() -> Dict[str, ToolDefinition]:
    """Obtener registro completo de herramientas"""
    return {
        "rag_search": ToolDefinition(
            name="rag_search",
            description="Búsqueda semántica en documentos usando RAG",
            tool_type=ToolType.RAG_SEARCH,
            parameters_schema=RAGSearchParams.model_json_schema(),
            response_schema=RAGSearchResponse.model_json_schema(),
            examples=[
                {
                    "query": "experiencia en microservicios",
                    "top_k": 3,
                    "document_type": "project"
                },
                {
                    "query": "certificaciones AWS",
                    "similarity_threshold": 0.8
                }
            ]
        ),
        "faq_query": ToolDefinition(
            name="faq_query",
            description="Consulta a base de preguntas frecuentes",
            tool_type=ToolType.FAQ_QUERY,
            parameters_schema=FAQQueryParams.model_json_schema(),
            response_schema=FAQQueryResponse.model_json_schema(),
            examples=[
                {
                    "query": "años de experiencia",
                    "category": "experiencia"
                },
                {
                    "query": "tecnologías principales",
                    "limit": 3
                }
            ]
        ),
        "send_notification": ToolDefinition(
            name="send_notification",
            description="Envío de notificaciones push",
            tool_type=ToolType.NOTIFICATION,
            parameters_schema=NotificationParams.model_json_schema(),
            response_schema=NotificationResponse.model_json_schema(),
            examples=[
                {
                    "message": "Nueva consulta sobre proyectos de banca",
                    "priority": "normal"
                }
            ]
        ),
        "combined_search": ToolDefinition(
            name="combined_search",
            description="Búsqueda combinada RAG + FAQ",
            tool_type=ToolType.COMBINED_SEARCH,
            parameters_schema=CombinedSearchParams.model_json_schema(),
            response_schema=CombinedSearchResponse.model_json_schema(),
            examples=[
                {
                    "query": "¿Qué experiencia tienes en cloud?",
                    "merge_strategy": "balanced"
                }
            ]
        )
    }

def main():
    """Función de test para schemas"""
    try:
        print("=== Tool Schemas Registry ===\n")
        
        # Mostrar todos los schemas
        schemas = get_all_tool_schemas()
        for schema in schemas:
            tool_name = schema["function"]["name"]
            description = schema["function"]["description"]
            print(f"Tool: {tool_name}")
            print(f"Description: {description}")
            print(f"Required params: {schema['function']['parameters'].get('required', [])}")
            print("-" * 50)
        
        # Mostrar registro de herramientas
        registry = get_tool_registry()
        print(f"\nTotal tools registered: {len(registry)}")
        
        for tool_name, tool_def in registry.items():
            print(f"\n{tool_name}:")
            print(f"  Type: {tool_def.tool_type}")
            print(f"  Examples: {len(tool_def.examples)}")
        
    except Exception as e:
        print(f"Error en test de schemas: {e}")
        raise

if __name__ == "__main__":
    main()