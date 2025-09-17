from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import cv_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Resume Roaster API",
    description="API que destruye CVs con humor y feedback constructivo",
    version="1.0.0",
    docs_url="/docs",
)

# Configurar CORS para conectar con el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Desarrollo local
        "",  #prod
        "*"  #por ahora permitimos todo
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Incluir las rutas del CV
app.include_router(cv_router.router, prefix="/api/v1", tags=["CV Processing"])

@app.get("/")
async def root():
    return {
        "message": "🔥 Resume Roaster API is alive!",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "upload": "/api/v1/upload-cv",
            "roast": "/api/v1/roast/{roast_id}"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "resume-roaster-api"}