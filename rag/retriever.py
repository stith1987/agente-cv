"""
RAG Retriever Module

Módulo para realizar búsquedas semánticas en la base de datos vectorial
de documentos del CV y proyectos.
"""

import os
from typing import List, Dict, Any, Optional
import logging
from dotenv import load_dotenv

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from dataclasses import dataclass

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

@dataclass
class SearchResult:
    """Clase para representar un resultado de búsqueda"""
    content: str
    metadata: Dict[str, Any]
    score: float
    chunk_id: str

class SemanticRetriever:
    """Clase para realizar búsquedas semánticas en documentos"""
    
    def __init__(self):
        """Inicializar el retriever"""
        self.vectordb_path = os.getenv("VECTORDB_PATH", "./storage/vectordb")
        self.top_k = int(os.getenv("TOP_K_RESULTS", "5"))
        self.similarity_threshold = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
        
        # Inicializar ChromaDB
        try:
            self.chroma_client = chromadb.PersistentClient(
                path=self.vectordb_path,
                settings=Settings(
                    anonymized_telemetry=False
                )
            )
            self.collection = self.chroma_client.get_collection("cv_documents")
            logger.info("Conexión a vector DB establecida")
        except Exception as e:
            logger.error(f"Error conectando a vector DB: {e}")
            raise
        
        # Inicializar modelo de embeddings (mismo que en ingesta)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info("Modelo de embeddings cargado")
    
    def search(
        self, 
        query: str, 
        top_k: Optional[int] = None,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Realizar búsqueda semántica
        
        Args:
            query: Consulta de búsqueda
            top_k: Número de resultados a retornar
            filter_metadata: Filtros de metadata (e.g., {"type": "project"})
        
        Returns:
            Lista de resultados ordenados por relevancia
        """
        if top_k is None:
            top_k = self.top_k
            
        try:
            # Generar embedding de la consulta
            query_embedding = self.embedding_model.encode([query]).tolist()[0]
            
            # Preparar filtros
            where_clause = {}
            if filter_metadata:
                where_clause.update(filter_metadata)
            
            # Realizar búsqueda en ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=where_clause if where_clause else None,
                include=["documents", "metadatas", "distances"]
            )
            
            # Convertir resultados al formato interno
            search_results = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    # ChromaDB retorna distancias, convertir a similarity score
                    distance = results['distances'][0][i]
                    similarity_score = 1 / (1 + distance)  # Convertir distancia a similarity
                    
                    # Filtrar por threshold si está configurado
                    if similarity_score >= self.similarity_threshold:
                        result = SearchResult(
                            content=results['documents'][0][i],
                            metadata=results['metadatas'][0][i],
                            score=similarity_score,
                            chunk_id=results['ids'][0][i] if 'ids' in results else f"chunk_{i}"
                        )
                        search_results.append(result)
            
            logger.info(f"Búsqueda realizada: {len(search_results)} resultados encontrados")
            return search_results
            
        except Exception as e:
            logger.error(f"Error en búsqueda semántica: {e}")
            raise
    
    def search_by_document_type(
        self, 
        query: str, 
        doc_type: str,
        top_k: Optional[int] = None
    ) -> List[SearchResult]:
        """
        Buscar en documentos de un tipo específico
        
        Args:
            query: Consulta de búsqueda
            doc_type: Tipo de documento ("cv", "project", "clip", "general")
            top_k: Número de resultados
        """
        return self.search(
            query=query,
            top_k=top_k,
            filter_metadata={"type": doc_type}
        )
    
    def search_in_projects(self, query: str, top_k: Optional[int] = None) -> List[SearchResult]:
        """Buscar específicamente en proyectos"""
        return self.search_by_document_type(query, "project", top_k)
    
    def search_in_cv(self, query: str, top_k: Optional[int] = None) -> List[SearchResult]:
        """Buscar específicamente en el CV"""
        return self.search_by_document_type(query, "cv", top_k)
    
    def search_in_clips(self, query: str, top_k: Optional[int] = None) -> List[SearchResult]:
        """Buscar específicamente en recortes/citas"""
        return self.search_by_document_type(query, "clip", top_k)
    
    def multi_query_search(self, queries: List[str], top_k: Optional[int] = None) -> Dict[str, List[SearchResult]]:
        """
        Realizar múltiples búsquedas y retornar resultados agrupados
        
        Args:
            queries: Lista de consultas
            top_k: Número de resultados por consulta
        
        Returns:
            Diccionario con resultados por consulta
        """
        results = {}
        for query in queries:
            results[query] = self.search(query, top_k)
        return results
    
    def get_similar_documents(self, chunk_id: str, top_k: Optional[int] = None) -> List[SearchResult]:
        """
        Encontrar documentos similares a un chunk específico
        
        Args:
            chunk_id: ID del chunk de referencia
            top_k: Número de resultados similares
        """
        if top_k is None:
            top_k = self.top_k
            
        try:
            # Obtener el chunk de referencia
            reference_result = self.collection.get(
                ids=[chunk_id],
                include=["documents", "embeddings"]
            )
            
            if not reference_result['embeddings']:
                raise ValueError(f"Chunk {chunk_id} no encontrado")
            
            # Usar el embedding del chunk para buscar similares
            reference_embedding = reference_result['embeddings'][0]
            
            results = self.collection.query(
                query_embeddings=[reference_embedding],
                n_results=top_k + 1,  # +1 porque incluirá el documento original
                include=["documents", "metadatas", "distances"]
            )
            
            # Excluir el documento original y convertir resultados
            search_results = []
            for i in range(len(results['documents'][0])):
                if results['ids'][0][i] != chunk_id:  # Excluir el original
                    distance = results['distances'][0][i]
                    similarity_score = 1 / (1 + distance)
                    
                    if similarity_score >= self.similarity_threshold:
                        result = SearchResult(
                            content=results['documents'][0][i],
                            metadata=results['metadatas'][0][i],
                            score=similarity_score,
                            chunk_id=results['ids'][0][i]
                        )
                        search_results.append(result)
            
            return search_results[:top_k]  # Limitar al top_k solicitado
            
        except Exception as e:
            logger.error(f"Error buscando documentos similares: {e}")
            raise
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de la base de datos"""
        try:
            total_count = self.collection.count()
            
            # Obtener sample de metadatos para análisis
            sample = self.collection.peek(limit=20)
            
            # Analizar tipos de documentos
            doc_types = {}
            if sample and sample['metadatas']:
                for metadata in sample['metadatas']:
                    doc_type = metadata.get('type', 'unknown')
                    doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
            
            return {
                "total_documents": total_count,
                "document_types": doc_types,
                "sample_size": len(sample['metadatas']) if sample else 0
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {"error": str(e)}
    
    def format_results_for_context(
        self, 
        results: List[SearchResult], 
        include_metadata: bool = True
    ) -> str:
        """
        Formatear resultados para usar como contexto en el LLM
        
        Args:
            results: Lista de resultados de búsqueda
            include_metadata: Si incluir información de metadata
            
        Returns:
            String formateado para contexto
        """
        if not results:
            return "No se encontraron documentos relevantes."
        
        formatted_context = []
        
        for i, result in enumerate(results, 1):
            context_block = f"--- Documento {i} ---\n"
            
            if include_metadata:
                context_block += f"Fuente: {result.metadata.get('filename', 'Unknown')}\n"
                context_block += f"Tipo: {result.metadata.get('type', 'Unknown')}\n"
                context_block += f"Relevancia: {result.score:.2f}\n\n"
            
            context_block += result.content
            context_block += f"\n{'='*50}\n"
            
            formatted_context.append(context_block)
        
        return "\n".join(formatted_context)

def main():
    """Función de ejemplo/test del retriever"""
    try:
        retriever = SemanticRetriever()
        
        # Estadísticas de la base de datos
        stats = retriever.get_database_stats()
        print("Estadísticas de la base de datos:")
        print(f"- Total documentos: {stats['total_documents']}")
        print(f"- Tipos de documentos: {stats['document_types']}")
        
        # Búsqueda de ejemplo
        query = "experiencia en arquitectura de microservicios"
        print(f"\nBúsqueda: '{query}'")
        results = retriever.search(query, top_k=3)
        
        for i, result in enumerate(results, 1):
            print(f"\nResultado {i}:")
            print(f"- Score: {result.score:.3f}")
            print(f"- Fuente: {result.metadata.get('filename', 'Unknown')}")
            print(f"- Tipo: {result.metadata.get('type', 'Unknown')}")
            print(f"- Contenido: {result.content[:200]}...")
        
    except Exception as e:
        logger.error(f"Error en test del retriever: {e}")
        raise

if __name__ == "__main__":
    main()