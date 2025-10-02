"""
Orchestrator Module

Orquestador principal que decide qué herramientas usar y cómo combinar
los resultados para proporcionar respuestas completas e inteligentes.
"""

import os
import json
from typing import Dict, Any, List, Optional, Tuple
import logging
from datetime import datetime
from dotenv import load_dotenv

# Imports de los módulos locales
from rag.retriever import SemanticRetriever
from tools.faq_sql import FAQSQLTool
from tools.notify import NotificationManager
from agent.prompts import (
    format_system_prompt,
    format_planning_prompt,
    format_classification_prompt,
    format_error_response,
    format_no_results_response
)

# Para LLM
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class QueryClassification:
    """Resultado de clasificación de consulta"""
    def __init__(self, data: Dict[str, Any]):
        self.category = data.get("category", "COMPLEX")
        self.confidence = data.get("confidence", 50)
        self.recommended_tool = data.get("recommended_tool", "COMBINED")
        self.reasoning = data.get("reasoning", "")
        self.search_terms = data.get("search_terms", [])
        self.expected_complexity = data.get("expected_complexity", "MEDIUM")

class CVOrchestrator:
    """Orquestador principal del agente de CV"""
    
    def __init__(self):
        """Inicializar el orquestador"""
        # Configuración
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4")
        self.openai_client = OpenAI(api_key=self.openai_api_key)
        
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY no está configurada")
        
        # Cliente OpenAI inicializado arriba
        
        # Inicializar herramientas
        try:
            self.retriever = SemanticRetriever()
            self.faq_tool = FAQSQLTool()
            self.notification_manager = NotificationManager()
            logger.info("Herramientas inicializadas correctamente")
        except Exception as e:
            logger.error(f"Error inicializando herramientas: {e}")
            raise
        
        # Stats y logs
        self.query_log = []
        self.session_stats = {
            "total_queries": 0,
            "rag_searches": 0,
            "faq_queries": 0,
            "combined_searches": 0,
            "errors": 0,
            "start_time": datetime.now()
        }
    
    def classify_query(self, query: str) -> QueryClassification:
        """
        Clasificar consulta para determinar estrategia de respuesta
        
        Args:
            query: Consulta del usuario
            
        Returns:
            Clasificación de la consulta
        """
        try:
            classification_prompt = format_classification_prompt(query)
            
            response = self.openai_client.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": classification_prompt},
                    {"role": "user", "content": f"Clasifica esta consulta: {query}"}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            # Parsear respuesta JSON
            content = response.choices[0].message.content
            
            # Extraer JSON de la respuesta
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                classification_data = json.loads(json_str)
                return QueryClassification(classification_data)
            else:
                logger.warning("No se pudo parsear clasificación, usando default")
                return QueryClassification({})
                
        except Exception as e:
            logger.error(f"Error en clasificación de consulta: {e}")
            return QueryClassification({})
    
    def search_rag(
        self,
        query: str,
        top_k: int = 5,
        document_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Realizar búsqueda RAG"""
        try:
            results = self.retriever.search(
                query=query,
                top_k=top_k,
                filter_metadata={"type": document_type} if document_type else None
            )
            
            self.session_stats["rag_searches"] += 1
            
            return {
                "success": True,
                "results": results,
                "total_found": len(results),
                "formatted_context": self.retriever.format_results_for_context(results)
            }
            
        except Exception as e:
            logger.error(f"Error en búsqueda RAG: {e}")
            return {
                "success": False,
                "error": str(e),
                "results": [],
                "total_found": 0,
                "formatted_context": ""
            }
    
    def search_faq(
        self,
        query: str,
        category: Optional[str] = None,
        limit: int = 5
    ) -> Dict[str, Any]:
        """Realizar búsqueda FAQ"""
        try:
            results = self.faq_tool.search_faqs(
                query=query,
                category=category,
                limit=limit
            )
            
            self.session_stats["faq_queries"] += 1
            
            return {
                "success": True,
                "results": results,
                "total_found": len(results),
                "formatted_results": self._format_faq_results(results)
            }
            
        except Exception as e:
            logger.error(f"Error en búsqueda FAQ: {e}")
            return {
                "success": False,
                "error": str(e),
                "results": [],
                "total_found": 0,
                "formatted_results": ""
            }
    
    def combined_search(
        self,
        query: str,
        include_rag: bool = True,
        include_faq: bool = True,
        merge_strategy: str = "relevance"
    ) -> Dict[str, Any]:
        """Realizar búsqueda combinada RAG + FAQ"""
        try:
            results = {
                "rag_results": None,
                "faq_results": None,
                "combined_summary": "",
                "total_sources": 0
            }
            
            # Búsqueda RAG
            if include_rag:
                rag_results = self.search_rag(query, top_k=3)
                results["rag_results"] = rag_results
                if rag_results["success"]:
                    results["total_sources"] += rag_results["total_found"]
            
            # Búsqueda FAQ
            if include_faq:
                faq_results = self.search_faq(query, limit=3)
                results["faq_results"] = faq_results
                if faq_results["success"]:
                    results["total_sources"] += faq_results["total_found"]
            
            # Combinar resultados según estrategia
            results["combined_summary"] = self._merge_results(
                results["rag_results"],
                results["faq_results"],
                merge_strategy
            )
            
            self.session_stats["combined_searches"] += 1
            
            return {
                "success": True,
                **results
            }
            
        except Exception as e:
            logger.error(f"Error en búsqueda combinada: {e}")
            return {
                "success": False,
                "error": str(e),
                "rag_results": None,
                "faq_results": None,
                "combined_summary": "",
                "total_sources": 0
            }
    
    def _merge_results(
        self,
        rag_results: Optional[Dict[str, Any]],
        faq_results: Optional[Dict[str, Any]],
        strategy: str = "relevance"
    ) -> str:
        """Combinar resultados de RAG y FAQ"""
        combined_content = []
        
        if strategy == "relevance":
            # Priorizar por relevancia/score
            all_results = []
            
            if rag_results and rag_results.get("success") and rag_results["results"]:
                for result in rag_results["results"][:2]:  # Top 2 RAG
                    all_results.append({
                        "content": result.content,
                        "score": result.score,
                        "type": "RAG",
                        "source": result.metadata.get("filename", "Unknown")
                    })
            
            if faq_results and faq_results.get("success") and faq_results["results"]:
                for result in faq_results["results"][:2]:  # Top 2 FAQ
                    all_results.append({
                        "content": f"Q: {result.question}\nA: {result.answer}",
                        "score": result.confidence,
                        "type": "FAQ",
                        "source": result.category
                    })
            
            # Ordenar por score y tomar los mejores
            all_results.sort(key=lambda x: x["score"], reverse=True)
            
            for i, result in enumerate(all_results[:3], 1):
                combined_content.append(
                    f"=== Fuente {i} ({result['type']}) ===\n"
                    f"Score: {result['score']:.2f}\n"
                    f"Origen: {result['source']}\n\n"
                    f"{result['content']}\n"
                )
        
        elif strategy == "type":
            # Separar por tipo
            if rag_results and rag_results.get("success"):
                combined_content.append("=== DOCUMENTOS (RAG) ===\n")
                combined_content.append(rag_results.get("formatted_context", ""))
                combined_content.append("\n")
            
            if faq_results and faq_results.get("success"):
                combined_content.append("=== PREGUNTAS FRECUENTES ===\n")
                combined_content.append(faq_results.get("formatted_results", ""))
        
        else:  # balanced
            # Alternar entre tipos
            rag_items = []
            faq_items = []
            
            if rag_results and rag_results.get("success") and rag_results["results"]:
                rag_items = rag_results["results"][:2]
            
            if faq_results and faq_results.get("success") and faq_results["results"]:
                faq_items = faq_results["results"][:2]
            
            max_items = max(len(rag_items), len(faq_items))
            
            for i in range(max_items):
                if i < len(rag_items):
                    result = rag_items[i]
                    combined_content.append(
                        f"=== Documento: {result.metadata.get('filename', 'Unknown')} ===\n"
                        f"{result.content}\n\n"
                    )
                
                if i < len(faq_items):
                    result = faq_items[i]
                    combined_content.append(
                        f"=== FAQ: {result.category} ===\n"
                        f"P: {result.question}\n"
                        f"R: {result.answer}\n\n"
                    )
        
        return "\n".join(combined_content) if combined_content else "No se encontraron resultados relevantes."
    
    def _format_faq_results(self, results: List[Any]) -> str:
        """Formatear resultados de FAQ para contexto"""
        if not results:
            return "No se encontraron FAQs relevantes."
        
        formatted = []
        for i, result in enumerate(results, 1):
            formatted.append(
                f"--- FAQ {i} ---\n"
                f"Categoría: {result.category}\n"
                f"Confianza: {result.confidence:.2f}\n"
                f"Pregunta: {result.question}\n"
                f"Respuesta: {result.answer}\n"
                f"{'='*50}\n"
            )
        
        return "\n".join(formatted)
    
    def generate_response(
        self,
        query: str,
        context: str,
        classification: Optional[QueryClassification] = None
    ) -> str:
        """
        Generar respuesta final usando LLM con contexto
        
        Args:
            query: Consulta del usuario
            context: Contexto obtenido de las herramientas
            classification: Clasificación de la consulta
        """
        try:
            system_prompt = format_system_prompt(include_tools=False)
            
            # Agregar contexto específico si está disponible
            if classification:
                system_prompt += f"\n\n## Contexto de la Consulta\n"
                system_prompt += f"Categoría: {classification.category}\n"
                system_prompt += f"Complejidad: {classification.expected_complexity}\n"
                system_prompt += f"Razonamiento: {classification.reasoning}\n"
            
            user_message = f"""
Consulta del usuario: {query}

Contexto disponible:
{context}

Por favor, proporciona una respuesta completa, precisa y profesional basada únicamente en el contexto proporcionado.
            """.strip()
            
            response = self.openai_client.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generando respuesta LLM: {e}")
            return format_error_response("LLM Error", str(e))
    
    def process_query(
        self,
        query: str,
        session_id: str = "anonymous",
        notify_important: bool = True
    ) -> Dict[str, Any]:
        """
        Procesar consulta completa del usuario
        
        Args:
            query: Consulta del usuario
            session_id: ID de sesión del usuario
            notify_important: Si enviar notificaciones para consultas importantes
            
        Returns:
            Respuesta completa con metadata
        """
        start_time = datetime.now()
        self.session_stats["total_queries"] += 1
        
        try:
            # 1. Clasificar consulta
            logger.info(f"Procesando consulta: {query[:50]}...")
            classification = self.classify_query(query)
            logger.info(f"Clasificación: {classification.category} ({classification.confidence}%)")
            
            # 2. Ejecutar estrategia según clasificación
            context = ""
            tool_results = {}
            
            if classification.recommended_tool == "FAQ_ONLY":
                faq_results = self.search_faq(query)
                context = faq_results.get("formatted_results", "")
                tool_results["faq"] = faq_results
                
            elif classification.recommended_tool == "RAG_ONLY":
                rag_results = self.search_rag(query)
                context = rag_results.get("formatted_context", "")
                tool_results["rag"] = rag_results
                
            else:  # COMBINED or default
                combined_results = self.combined_search(query)
                context = combined_results.get("combined_summary", "")
                tool_results["combined"] = combined_results
            
            # 3. Verificar si tenemos contexto útil
            if not context or context.strip() == "" or "No se encontraron" in context:
                # Intentar búsqueda más amplia
                logger.warning("Contexto vacío, intentando búsqueda amplia")
                backup_results = self.combined_search(query, merge_strategy="balanced")
                context = backup_results.get("combined_summary", "")
                tool_results["backup"] = backup_results
            
            # 4. Generar respuesta final
            if context and context.strip():
                response_text = self.generate_response(query, context, classification)
            else:
                response_text = format_no_results_response(
                    query,
                    alternatives=["Reformula tu pregunta de manera más específica"],
                    related_topics=["Experiencia técnica", "Proyectos destacados", "Competencias"]
                )
            
            # 5. Calcular métricas
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # 6. Enviar notificación si es importante
            if notify_important and classification.confidence > 80:
                try:
                    self.notification_manager.send_query_notification(
                        user_query=query,
                        response_summary=response_text[:150],
                        session_id=session_id
                    )
                except Exception as e:
                    logger.warning(f"Error enviando notificación: {e}")
            
            # 7. Log de la consulta
            query_log_entry = {
                "timestamp": start_time,
                "session_id": session_id,
                "query": query,
                "classification": {
                    "category": classification.category,
                    "confidence": classification.confidence,
                    "tool": classification.recommended_tool
                },
                "processing_time": processing_time,
                "context_length": len(context),
                "response_length": len(response_text),
                "success": True
            }
            self.query_log.append(query_log_entry)
            
            return {
                "success": True,
                "response": response_text,
                "metadata": {
                    "classification": classification.__dict__,
                    "processing_time": processing_time,
                    "tools_used": list(tool_results.keys()),
                    "context_length": len(context),
                    "session_id": session_id
                },
                "tool_results": tool_results
            }
            
        except Exception as e:
            # Manejo de errores
            logger.error(f"Error procesando consulta: {e}")
            self.session_stats["errors"] += 1
            
            error_response = format_error_response("Processing Error", str(e))
            
            # Log del error
            error_log_entry = {
                "timestamp": start_time,
                "session_id": session_id,
                "query": query,
                "error": str(e),
                "processing_time": (datetime.now() - start_time).total_seconds(),
                "success": False
            }
            self.query_log.append(error_log_entry)
            
            # Notificar error crítico
            try:
                self.notification_manager.send_error_notification(
                    error_message=str(e),
                    context={"query": query, "session_id": session_id}
                )
            except:
                pass  # No fallar si la notificación falla
            
            return {
                "success": False,
                "response": error_response,
                "error": str(e),
                "metadata": {
                    "processing_time": (datetime.now() - start_time).total_seconds(),
                    "session_id": session_id
                }
            }
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de la sesión"""
        uptime = (datetime.now() - self.session_stats["start_time"]).total_seconds()
        
        return {
            **self.session_stats,
            "uptime_seconds": uptime,
            "success_rate": (
                (self.session_stats["total_queries"] - self.session_stats["errors"]) 
                / max(self.session_stats["total_queries"], 1)
            ) * 100,
            "avg_processing_time": (
                sum(log["processing_time"] for log in self.query_log if log.get("success"))
                / max(len([log for log in self.query_log if log.get("success")]), 1)
            ),
            "recent_queries": [
                {
                    "query": log["query"],
                    "timestamp": log["timestamp"].isoformat(),
                    "success": log["success"]
                }
                for log in self.query_log[-5:]
            ]
        }

def main():
    """Función de test para el orquestador"""
    try:
        print("=== Inicializando CV Orchestrator ===")
        orchestrator = CVOrchestrator()
        
        # Consultas de test
        test_queries = [
            "¿Cuáles son mis principales tecnologías?",
            "Cuéntame sobre el proyecto de banca digital",
            "¿Qué certificaciones tengo?",
            "¿Cuántos años de experiencia tengo en microservicios?"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{'='*60}")
            print(f"TEST {i}: {query}")
            print(f"{'='*60}")
            
            result = orchestrator.process_query(query, session_id=f"test_{i}")
            
            if result["success"]:
                print(f"✅ Respuesta generada:")
                print(f"Longitud: {len(result['response'])} caracteres")
                print(f"Herramientas: {result['metadata']['tools_used']}")
                print(f"Tiempo: {result['metadata']['processing_time']:.2f}s")
                print(f"Clasificación: {result['metadata']['classification']['category']}")
                print(f"\nRespuesta: {result['response'][:200]}...")
            else:
                print(f"❌ Error: {result['error']}")
        
        # Estadísticas finales
        print(f"\n{'='*60}")
        print("ESTADÍSTICAS DE SESIÓN")
        print(f"{'='*60}")
        stats = orchestrator.get_session_stats()
        
        print(f"Total consultas: {stats['total_queries']}")
        print(f"Búsquedas RAG: {stats['rag_searches']}")
        print(f"Consultas FAQ: {stats['faq_queries']}")
        print(f"Búsquedas combinadas: {stats['combined_searches']}")
        print(f"Errores: {stats['errors']}")
        print(f"Tasa de éxito: {stats['success_rate']:.1f}%")
        print(f"Tiempo promedio: {stats['avg_processing_time']:.2f}s")
        print(f"Tiempo activo: {stats['uptime_seconds']:.1f}s")
        
    except Exception as e:
        logger.error(f"Error en test del orquestador: {e}")
        raise

if __name__ == "__main__":
    main()