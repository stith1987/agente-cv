"""
FAQ SQL Tool

Herramienta para consultar una base de datos SQLite con preguntas frecuentes
sobre el CV y la experiencia profesional.
"""

import os
import sqlite3
from typing import List, Dict, Any, Optional
import logging
from dotenv import load_dotenv
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

@dataclass
class FAQResult:
    """Resultado de consulta FAQ"""
    question: str
    answer: str
    category: str
    tags: List[str]
    confidence: float

class FAQSQLTool:
    """Herramienta para consultas SQL a base de FAQs"""
    
    def __init__(self):
        """Inicializar la herramienta SQL"""
        self.db_path = os.getenv("SQLITE_DB_PATH", "./storage/sqlite/faq.db")
        self.ensure_database_exists()
        
    def ensure_database_exists(self):
        """Crear la base de datos y tablas si no existen"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS faqs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    category TEXT,
                    tags TEXT,  -- JSON string con tags
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS faq_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    faq_id INTEGER,
                    query TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_session TEXT,
                    FOREIGN KEY (faq_id) REFERENCES faqs (id)
                )
            """)
            
            # Crear índices para búsquedas eficientes
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_faqs_category ON faqs(category)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_faqs_question_fts ON faqs(question)
            """)
            
            conn.commit()
        
        # Insertar datos de ejemplo si la tabla está vacía
        self._insert_sample_data()
        logger.info("Base de datos FAQ inicializada")
    
    def _insert_sample_data(self):
        """Insertar datos de ejemplo en la base de FAQs"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Verificar si ya hay datos
            cursor.execute("SELECT COUNT(*) FROM faqs")
            if cursor.fetchone()[0] > 0:
                return
            
            sample_faqs = [
                {
                    "question": "¿Cuáles son mis principales tecnologías?",
                    "answer": "Mis principales tecnologías incluyen Java/Spring Boot, Python, React, AWS, Docker, Kubernetes, PostgreSQL, y arquitecturas de microservicios.",
                    "category": "tecnologias",
                    "tags": '["java", "python", "react", "aws", "microservicios"]'
                },
                {
                    "question": "¿Cuántos años de experiencia tengo?",
                    "answer": "Tengo más de 10 años de experiencia en desarrollo de software y arquitectura de soluciones, con especialización en transformación digital.",
                    "category": "experiencia",
                    "tags": '["experiencia", "años", "trayectoria"]'
                },
                {
                    "question": "¿En qué sectores he trabajado?",
                    "answer": "He trabajado principalmente en el sector financiero, específicamente en banca digital, pagos, y servicios financieros. También tengo experiencia en e-commerce y tecnología empresarial.",
                    "category": "industria",
                    "tags": '["fintech", "banca", "pagos", "ecommerce"]'
                },
                {
                    "question": "¿Qué certificaciones tengo?",
                    "answer": "Poseo certificaciones como AWS Solutions Architect Professional, Google Cloud Professional Cloud Architect, Certified Kubernetes Administrator (CKA), y Spring Professional Certification.",
                    "category": "certificaciones",
                    "tags": '["aws", "gcp", "kubernetes", "spring", "certificaciones"]'
                },
                {
                    "question": "¿Cuál es mi educación?",
                    "answer": "Tengo una Maestría en Arquitectura de Software y soy Ingeniero en Sistemas de Información, graduado Magna Cum Laude.",
                    "category": "educacion",
                    "tags": '["maestria", "ingenieria", "educacion", "universidad"]'
                },
                {
                    "question": "¿Qué proyectos destacados he liderado?",
                    "answer": "He liderado la arquitectura de una plataforma de banca digital que sirve a más de 2M de usuarios y el diseño de un marco de arquitectura empresarial para una corporación multinacional.",
                    "category": "proyectos",
                    "tags": '["banca digital", "arquitectura empresarial", "liderazgo"]'
                },
                {
                    "question": "¿Qué metodologías de trabajo domino?",
                    "answer": "Domino metodologías ágiles como Scrum, Design Thinking, Lean Startup, y prácticas de DevOps. También tengo experiencia con frameworks de arquitectura como TOGAF.",
                    "category": "metodologias",
                    "tags": '["agile", "scrum", "devops", "togaf", "metodologias"]'
                },
                {
                    "question": "¿He publicado artículos o dado conferencias?",
                    "answer": "Sí, he publicado artículos sobre microservicios y arquitectura event-driven, y he sido speaker en DevOps Days y Tech Summit, presentando sobre transformación de monolitos a microservicios.",
                    "category": "publicaciones",
                    "tags": '["articulos", "conferencias", "speaker", "devops"]'
                },
                {
                    "question": "¿Qué idiomas hablo?",
                    "answer": "Hablo español (nativo), inglés a nivel profesional (C1), y portugués a nivel intermedio (B2).",
                    "category": "idiomas",
                    "tags": '["español", "ingles", "portugues", "idiomas"]'
                },
                {
                    "question": "¿Cuáles son mis fortalezas como arquitecto?",
                    "answer": "Mis fortalezas incluyen el diseño de arquitecturas escalables, liderazgo técnico, mentoreo de equipos, optimización de performance, y la capacidad de traducir requerimientos de negocio en soluciones técnicas efectivas.",
                    "category": "fortalezas",
                    "tags": '["liderazgo", "escalabilidad", "mentoring", "performance"]'
                }
            ]
            
            for faq in sample_faqs:
                cursor.execute("""
                    INSERT INTO faqs (question, answer, category, tags)
                    VALUES (?, ?, ?, ?)
                """, (faq["question"], faq["answer"], faq["category"], faq["tags"]))
            
            conn.commit()
            logger.info(f"Insertadas {len(sample_faqs)} FAQs de ejemplo")
    
    def search_faqs(
        self, 
        query: str, 
        category: Optional[str] = None,
        limit: int = 5
    ) -> List[FAQResult]:
        """
        Buscar FAQs que coincidan con la consulta
        
        Args:
            query: Texto de búsqueda
            category: Filtrar por categoría específica
            limit: Número máximo de resultados
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Construir consulta SQL con búsqueda de texto
            sql = """
                SELECT id, question, answer, category, tags,
                       (CASE 
                        WHEN question LIKE ? THEN 10
                        WHEN answer LIKE ? THEN 5
                        WHEN tags LIKE ? THEN 3
                        ELSE 1
                       END) as relevance_score
                FROM faqs 
                WHERE is_active = 1
            """
            
            params = [f"%{query}%", f"%{query}%", f"%{query}%"]
            
            if category:
                sql += " AND category = ?"
                params.append(category)
            
            sql += " ORDER BY relevance_score DESC, id ASC LIMIT ?"
            params.append(limit)
            
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            results = []
            for row in rows:
                # Parse tags JSON
                import json
                try:
                    tags = json.loads(row['tags']) if row['tags'] else []
                except:
                    tags = []
                
                # Calcular confidence basado en coincidencias
                confidence = self._calculate_confidence(query, row['question'], row['answer'])
                
                result = FAQResult(
                    question=row['question'],
                    answer=row['answer'],
                    category=row['category'],
                    tags=tags,
                    confidence=confidence
                )
                results.append(result)
                
                # Registrar analíticas
                self._log_query_analytics(row['id'], query)
            
            logger.info(f"FAQ search: '{query}' -> {len(results)} resultados")
            return results
    
    def _calculate_confidence(self, query: str, question: str, answer: str) -> float:
        """Calcular nivel de confianza de la coincidencia"""
        query_lower = query.lower()
        question_lower = question.lower()
        answer_lower = answer.lower()
        
        confidence = 0.0
        
        # Coincidencia exacta en pregunta
        if query_lower in question_lower:
            confidence += 0.8
        
        # Coincidencia exacta en respuesta
        if query_lower in answer_lower:
            confidence += 0.6
        
        # Coincidencias de palabras individuales
        query_words = set(query_lower.split())
        question_words = set(question_lower.split())
        answer_words = set(answer_lower.split())
        
        question_overlap = len(query_words.intersection(question_words)) / len(query_words)
        answer_overlap = len(query_words.intersection(answer_words)) / len(query_words)
        
        confidence += question_overlap * 0.4
        confidence += answer_overlap * 0.3
        
        return min(confidence, 1.0)  # Max 1.0
    
    def _log_query_analytics(self, faq_id: int, query: str, user_session: str = "anonymous"):
        """Registrar analytics de consultas"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO faq_analytics (faq_id, query, user_session)
                    VALUES (?, ?, ?)
                """, (faq_id, query, user_session))
                conn.commit()
        except Exception as e:
            logger.warning(f"Error registrando analytics: {e}")
    
    def get_categories(self) -> List[str]:
        """Obtener todas las categorías disponibles"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT category FROM faqs WHERE is_active = 1 ORDER BY category")
            return [row[0] for row in cursor.fetchall()]
    
    def get_faq_by_id(self, faq_id: int) -> Optional[FAQResult]:
        """Obtener FAQ específica por ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT question, answer, category, tags
                FROM faqs 
                WHERE id = ? AND is_active = 1
            """, (faq_id,))
            
            row = cursor.fetchone()
            if row:
                import json
                tags = json.loads(row['tags']) if row['tags'] else []
                
                return FAQResult(
                    question=row['question'],
                    answer=row['answer'],
                    category=row['category'],
                    tags=tags,
                    confidence=1.0
                )
        return None
    
    def add_faq(
        self, 
        question: str, 
        answer: str, 
        category: str = "general",
        tags: List[str] = None
    ) -> int:
        """Agregar nueva FAQ"""
        if tags is None:
            tags = []
        
        import json
        tags_json = json.dumps(tags)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO faqs (question, answer, category, tags)
                VALUES (?, ?, ?, ?)
            """, (question, answer, category, tags_json))
            
            faq_id = cursor.lastrowid
            conn.commit()
            
            logger.info(f"Nueva FAQ agregada con ID: {faq_id}")
            return faq_id
    
    def get_analytics_summary(self) -> Dict[str, Any]:
        """Obtener resumen de analytics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total consultas
            cursor.execute("SELECT COUNT(*) FROM faq_analytics")
            total_queries = cursor.fetchone()[0]
            
            # FAQs más consultadas
            cursor.execute("""
                SELECT f.question, COUNT(*) as query_count
                FROM faq_analytics a
                JOIN faqs f ON a.faq_id = f.id
                GROUP BY a.faq_id
                ORDER BY query_count DESC
                LIMIT 5
            """)
            popular_faqs = cursor.fetchall()
            
            # Consultas recientes
            cursor.execute("""
                SELECT query, timestamp
                FROM faq_analytics
                ORDER BY timestamp DESC
                LIMIT 10
            """)
            recent_queries = cursor.fetchall()
            
            return {
                "total_queries": total_queries,
                "popular_faqs": popular_faqs,
                "recent_queries": recent_queries
            }

def main():
    """Función de test para la herramienta FAQ"""
    try:
        faq_tool = FAQSQLTool()
        
        # Test búsquedas
        test_queries = [
            "experiencia en AWS",
            "certificaciones",
            "proyectos de banca",
            "tecnologías que domino"
        ]
        
        for query in test_queries:
            print(f"\n--- Búsqueda: '{query}' ---")
            results = faq_tool.search_faqs(query, limit=3)
            
            for i, result in enumerate(results, 1):
                print(f"{i}. [{result.category}] {result.question}")
                print(f"   Confianza: {result.confidence:.2f}")
                print(f"   Respuesta: {result.answer[:100]}...")
        
        # Mostrar categorías
        print(f"\nCategorías disponibles: {faq_tool.get_categories()}")
        
        # Analytics
        analytics = faq_tool.get_analytics_summary()
        print(f"\nTotal consultas registradas: {analytics['total_queries']}")
        
    except Exception as e:
        logger.error(f"Error en test FAQ: {e}")
        raise

if __name__ == "__main__":
    main()