import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Support module path resolution
base_dir = Path(__file__).resolve().parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from app.core.config import settings
from app.database.database import engine, Base
from app.api.routes import health, screening, history

# Initialize Database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise-grade Explainable AI for Automated Diabetic Retinopathy Screening API"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static & Reports mounting
app.mount("/reports", StaticFiles(directory=str(settings.REPORTS_DIR)), name="reports")

# Include Routers
app.include_router(health.router, prefix=settings.API_V1_STR, tags=["Health"])
app.include_router(screening.router, prefix=settings.API_V1_STR, tags=["Screening"])
app.include_router(history.router, prefix=settings.API_V1_STR, tags=["History"])

@app.get("/")
async def root():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "disclaimer": settings.MEDICAL_DISCLAIMER
    }
