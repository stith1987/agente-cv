"""
RAG Document Ingestion Module

Este módulo se encarga de cargar, procesar y vectorizar documentos markdown
del CV y proyectos para crear un índice de búsqueda semántica.
"""

import os
import glob
from pathlib import Path
from typing import List, Dict, Any
import logging
from dotenv import load_dotenv

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import markdown
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class DocumentIngestor:
    """Clase para ingestar y vectorizar documentos markdown"""
    
    def __init__(self):
        """Inicializar el ingestor con configuraciones por defecto"""
        self.vectordb_path = os.getenv("VECTORDB_PATH", "./storage/vectordb")
        self.chunk_size = int(os.getenv("CHUNK_SIZE", "1000"))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "200"))
        
        # Inicializar componentes
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
        )
        
        # Inicializar ChromaDB
        self.chroma_client = chromadb.PersistentClient(
            path=self.vectordb_path,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Crear colección
        try:
            self.collection = self.chroma_client.get_collection("cv_documents")
            logger.info("Colección existente encontrada")
        except Exception:
            self.collection = self.chroma_client.create_collection(
                name="cv_documents",
                metadata={"description": "CV and projects documents"}
            )
            logger.info("Nueva colección creada")
        
        # Inicializar modelo de embeddings
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info("Modelo de embeddings cargado")
    
    def load_markdown_files(self, data_dir: str = "./data") -> List[Document]:
        """Cargar todos los archivos markdown del directorio de datos"""
        documents = []
        
        # Patterns para diferentes tipos de archivos
        patterns = [
            os.path.join(data_dir, "*.md"),
            os.path.join(data_dir, "proyectos", "*.md"),
            os.path.join(data_dir, "recortes", "*.md"),
        ]
        
        for pattern in patterns:
            for file_path in glob.glob(pattern):
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        
                    # Convertir markdown a texto plano
                    html = markdown.markdown(content)
                    # Para simplificar, usamos el contenido markdown directamente
                    
                    # Crear documento con metadata
                    relative_path = os.path.relpath(file_path, data_dir)
                    doc_type = self._get_document_type(relative_path)
                    
                    document = Document(
                        page_content=content,
                        metadata={
                            "source": file_path,
                            "relative_path": relative_path,
                            "type": doc_type,
                            "filename": os.path.basename(file_path)
                        }
                    )
                    documents.append(document)
                    logger.info(f"Cargado: {relative_path}")
                    
                except Exception as e:
                    logger.error(f"Error cargando {file_path}: {e}")
        
        logger.info(f"Total documentos cargados: {len(documents)}")
        return documents
    
    def _get_document_type(self, relative_path: str) -> str:
        """Determinar el tipo de documento basado en la ruta"""
        if "proyectos" in relative_path:
            return "project"
        elif "recortes" in relative_path:
            return "clip"
        elif relative_path == "cv.md":
            return "cv"
        else:
            return "general"
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Dividir documentos en chunks más pequeños"""
        all_chunks = []
        
        for doc in documents:
            chunks = self.text_splitter.split_documents([doc])
            
            # Agregar metadata adicional a cada chunk
            for i, chunk in enumerate(chunks):
                chunk.metadata.update({
                    "chunk_id": f"{doc.metadata['filename']}_{i}",
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                })
                all_chunks.append(chunk)
        
        logger.info(f"Total chunks creados: {len(all_chunks)}")
        return all_chunks
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generar embeddings para una lista de textos"""
        try:
            embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generando embeddings: {e}")
            raise
    
    def store_in_vectordb(self, chunks: List[Document]) -> None:
        """Almacenar chunks con sus embeddings en ChromaDB"""
        # Limpiar colección existente
        try:
            self.collection.delete()
            logger.info("Colección limpiada")
        except Exception:
            pass
        
        # Preparar datos para inserción
        texts = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        ids = [chunk.metadata["chunk_id"] for chunk in chunks]
        
        # Generar embeddings
        logger.info("Generando embeddings...")
        embeddings = self.generate_embeddings(texts)
        
        # Insertar en ChromaDB en batches
        batch_size = 100
        for i in range(0, len(chunks), batch_size):
            batch_end = min(i + batch_size, len(chunks))
            
            self.collection.add(
                embeddings=embeddings[i:batch_end],
                documents=texts[i:batch_end],
                metadatas=metadatas[i:batch_end],
                ids=ids[i:batch_end]
            )
            
            logger.info(f"Batch {i//batch_size + 1} insertado ({batch_end}/{len(chunks)})")
        
        logger.info("Todos los documentos almacenados en vector DB")
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de la colección"""
        count = self.collection.count()
        
        # Obtener algunos documentos para análisis
        sample = self.collection.peek(limit=10) if count > 0 else None
        
        return {
            "total_documents": count,
            "sample_metadata": sample["metadatas"] if sample else []
        }
    
    def ingest_all(self, data_dir: str = "./data") -> Dict[str, Any]:
        """Proceso completo de ingesta de documentos"""
        logger.info("Iniciando proceso de ingesta...")
        
        # 1. Cargar documentos markdown
        documents = self.load_markdown_files(data_dir)
        if not documents:
            raise ValueError("No se encontraron documentos para procesar")
        
        # 2. Dividir en chunks
        chunks = self.chunk_documents(documents)
        
        # 3. Almacenar en vector DB
        self.store_in_vectordb(chunks)
        
        # 4. Obtener estadísticas
        stats = self.get_collection_stats()
        
        logger.info("Proceso de ingesta completado")
        return {
            "status": "success",
            "documents_processed": len(documents),
            "chunks_created": len(chunks),
            "vector_db_stats": stats
        }

def main():
    """Función principal para ejecutar la ingesta"""
    try:
        ingestor = DocumentIngestor()
        result = ingestor.ingest_all()
        
        print("\n" + "="*50)
        print("RESUMEN DE INGESTA")
        print("="*50)
        print(f"Documentos procesados: {result['documents_processed']}")
        print(f"Chunks creados: {result['chunks_created']}")
        print(f"Total en vector DB: {result['vector_db_stats']['total_documents']}")
        print("="*50)
        
        return result
        
    except Exception as e:
        logger.error(f"Error en el proceso de ingesta: {e}")
        raise

if __name__ == "__main__":
    main()