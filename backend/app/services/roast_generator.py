import hashlib
import uuid
from datetime import datetime
from typing import Dict, Any
import time
from app.services.ai_service import AIService
from app.services.pdf_processor import PDFProcessor

class RoastGenerator:
    def __init__(self):
        """Inicializa el generador de roasts"""
        self.ai_service = AIService()
        self.pdf_processor = PDFProcessor()
        
        #Cache en memoria para evitar reprocesar CVs idénticos
        self._cache = {}
        
    async def process_cv_file(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """
        Procesa un CV completo: extrae texto, genera roast y feedback
        Args:
            file_content: Contenido del archivo en bytes
            filename: Nombre del archivo
        Returns:
            Dict con todo el resultado del roast
        """
        start_time = time.time()
        
        try:
            #Validar tamaño del archivo
            if not self.pdf_processor.validate_file_size(file_content):
                raise ValueError("Archivo muy grande (máximo 5MB)")
            
            #Generar ID único para este roast
            roast_id = self._generate_roast_id(file_content, filename)
            
            #Verificar cache (para ahorrar API calls)
            if roast_id in self._cache:
                cached_result = self._cache[roast_id].copy()
                cached_result["from_cache"] = True
                return cached_result
            
            cv_text = await self.pdf_processor.extract_text_from_file(
                file_content, filename
            ) #extraemos el texto 
            
            #Validar que el texto no esté vacío
            if len(cv_text.strip()) < 50:
                raise ValueError("El CV parece estar vacío o tener muy poco contenido")
            
            #Generar roast con IA
            ai_result = await self.ai_service.generate_roast_and_feedback(cv_text)
            
            processing_time = time.time() - start_time #cerramos para ver tiempo total
            
            result = {
                "roast_id": roast_id,
                "roast_text": ai_result["roast"],
                "feedback_points": ai_result["feedback"],
                "brutality_level": ai_result["brutality_level"],
                "processing_time": round(processing_time, 2),
                "created_at": datetime.now().isoformat(),
                "cv_length": len(cv_text),
                "feedback_count": len(ai_result["feedback"]),
                "from_cache": False
            }
            
            self._add_to_cache(roast_id, result) #guardamos en caché
            
            return result
            
        except Exception as e:
            raise Exception(f"Error procesando tu CV: {str(e)}")

    def _generate_roast_id(self, file_content: bytes, filename: str) -> str:
        #Hash del contenido + timestamp para uniqueness
        content_hash = hashlib.md5(file_content).hexdigest()[:8]
        timestamp = str(int(time.time()))[-6:]  #últimos 6 dígitos
        
        return f"roast-{content_hash}-{timestamp}"

    def _add_to_cache(self, roast_id: str, result: Dict[str, Any]) -> None:
        #Limitar cache a 100 entries (para no consumir mucha memoria)
        if len(self._cache) >= 100:
            oldest_key = next(iter(self._cache)) #removemos la entrada más antigua
            del self._cache[oldest_key]
        
        self._cache[roast_id] = result.copy()

    def get_roast_by_id(self, roast_id: str) -> Dict[str, Any]:
        if roast_id not in self._cache:
            raise ValueError("Roast no encontrado o expirado")
        
        return self._cache[roast_id].copy()

    def get_cache_stats(self) -> Dict[str, int]:
        return {
            "cached_roasts": len(self._cache),  
            "cache_limit": 100
        }