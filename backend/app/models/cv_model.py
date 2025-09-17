from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

#Respuesta del upload
class UploadResponse(BaseModel):
    roast_id: str
    message: str
    processing_status: str
    estimated_time: int  # segundos

#Resultado del roast
class RoastResult(BaseModel):
    roast_id: str
    roast_text: str
    feedback_points: List[str]
    brutality_level: int  # 1-100
    processing_time: float  # segundos
    created_at: datetime
    
#Errores
class ErrorResponse(BaseModel):
    error: str
    message: str
    roast_id: Optional[str] = None

#Stats del roast
class RoastStats(BaseModel):
    brutality_level: int
    processing_time: float
    feedback_count: int