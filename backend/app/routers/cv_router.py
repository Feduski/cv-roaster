from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import time
from typing import Dict, Any

from app.models.cv_model import UploadResponse, RoastResult, ErrorResponse
from app.services.roast_generator import RoastGenerator

router = APIRouter()
 
roast_generator = RoastGenerator() #instancia global del generador (se usa entre requests)
roast_storage: Dict[str, Dict[str, Any]] = {} #storage en memoria para los resultados (temporal)

@router.post("/upload-cv", response_model=UploadResponse)
async def upload_cv(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Endpoint principal: sube un CV y devuelve el roast
    Procesa todo en el momento (no background job)
    """
    start_time = time.time()
    
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No se subió ningún archivo")        
        if not file.filename:
            raise HTTPException(status_code=400, detail="Archivo sin nombre")
        
        #validar extensión
        allowed_extensions = ['.pdf', '.doc', '.docx']
        if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
            raise HTTPException(status_code=400, detail="Formato no soportado. Solo PDF, DOC, DOCX"           )
        
        file_content = await file.read()
        
        if len(file_content) == 0:
            raise HTTPException(status_code=400, detail="El archivo está vacío")
        
        #procesamos el cv (extraer texto + generar roast)
        result = await roast_generator.process_cv_file(file_content, file.filename)
        
        roast_storage[result["roast_id"]] = result #guardamos el resultado en memoria temporal
        
        total_time = time.time() - start_time #cerramos tiempo
        
        return UploadResponse(
            roast_id=result["roast_id"], message="¡CV roasteado exitosamente! 🔥",
            processing_status="completed", estimated_time=int(total_time)
        )
        
    except HTTPException:
        raise
        
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error procesando tu CV: {str(e)}")

@router.get("/roast/{roast_id}", response_model=RoastResult)
async def get_roast(roast_id: str):
    """Obtiene el resultado de un roast por ID"""
    try:
        if roast_id not in roast_storage:
            #intentar buscar en cache del generator
            try:
                result = roast_generator.get_roast_by_id(roast_id)
                roast_storage[roast_id] = result #sincronizar storages con el faltante
            except ValueError:
                raise HTTPException(status_code=404,detail="Roast no encontrado. Puede haber expirado.")
        
        result = roast_storage[roast_id]
        return RoastResult(
            roast_id=result["roast_id"],
            roast_text=result["roast_text"],
            feedback_points=result["feedback_points"],
            brutality_level=result["brutality_level"],
            processing_time=result["processing_time"],
            created_at=result["created_at"]
        )
        
    except HTTPException:
        raise
        
    except Exception as e:
        print(f"Error obteniendo roast: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/roast/{roast_id}/stats")
async def get_roast_stats(roast_id: str):
    """Obtiene estadísticas adicionales de un roast"""
    try:
        if roast_id not in roast_storage:
            raise HTTPException(status_code=404, detail="Roast no encontrado")
        
        result = roast_storage[roast_id]
        
        return {
            "roast_id": roast_id,
            "brutality_level": result["brutality_level"],
            "processing_time": result["processing_time"],
            "feedback_count": result["feedback_count"],
            "cv_length": result.get("cv_length", 0),
            "from_cache": result.get("from_cache", False),
            "created_at": result["created_at"]
        }
        
    except HTTPException:
        raise
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error obteniendo estadísticas")

@router.delete("/roast/{roast_id}")
async def delete_roast(roast_id: str):
    """Elimina un roast del storage (para limpiar memoria)"""
    try:
        if roast_id in roast_storage:
            del roast_storage[roast_id]
            return {"message": f"Roast {roast_id} eliminado"}
        else:
            raise HTTPException(status_code=404, detail="Roast no encontrado")
            
    except HTTPException:
        raise
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error eliminando roast")

@router.get("/health")
async def health_check():
    """Health check específico para el CV router"""
    try:
        # Verificar que todos los servicios estén OK
        cache_stats = roast_generator.get_cache_stats()
        
        return {
            "status": "healthy",
            "service": "cv-router",
            "active_roasts": len(roast_storage),
            "cache_stats": cache_stats,
            "endpoints": {
                "upload": "/api/v1/upload-cv",
                "get_roast": "/api/v1/roast/{roast_id}",
                "stats": "/api/v1/roast/{roast_id}/stats"
            }
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "unhealthy", "error": str(e)}
        )

@router.post("/admin/clear-storage")
async def clear_storage():
    """Limpia todo el storage temporal"""
    try:
        cleared_count = len(roast_storage)
        roast_storage.clear()
        
        return {
            "message": f"Storage limpiado. {cleared_count} roasts eliminados.",
            "remaining_roasts": len(roast_storage)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error limpiando storage")