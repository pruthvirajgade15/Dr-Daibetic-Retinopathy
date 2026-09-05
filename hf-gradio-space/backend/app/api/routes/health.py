from fastapi import APIRouter
from ...core.config import settings
from ...schemas.response import HealthResponse
from ...ml.model import load_dr_model

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    model = load_dr_model()
    return HealthResponse(
        status="online",
        service=settings.PROJECT_NAME,
        version=settings.VERSION,
        model_loaded=model is not None,
        disclaimer=settings.MEDICAL_DISCLAIMER
    )
