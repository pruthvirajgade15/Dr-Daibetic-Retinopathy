from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class PatientInfo(BaseModel):
    patient_id: str = Field(default="ANON_PATIENT", description="Clinical patient identifier")
    eye: str = Field(default="OD", description="Eye side: OD (Right) or OS (Left)")
    age: Optional[int] = Field(default=None, description="Patient age in years")

class QualityScoreResponse(BaseModel):
    overall_quality_score: float
    sharpness_score: float
    illumination_score: float
    contrast_score: float
    status: str
    is_gradable: bool

class PredictionDetail(BaseModel):
    grade: int
    stage: str
    confidence: float
    is_referable: bool
    clinical_urgency: str
    probabilities: Dict[str, float]

class ExplainabilityDetail(BaseModel):
    dominant_quadrant: str
    quadrants: Dict[str, float]

class MultiModalImages(BaseModel):
    original: str
    preprocessed: str
    gradcam: str
    structures: str

class ScreeningResponse(BaseModel):
    id: str
    status: str
    patient_id: str
    eye: str
    age: Optional[int]
    created_at: str
    quality: QualityScoreResponse
    prediction: PredictionDetail
    explainability: ExplainabilityDetail
    images: MultiModalImages
    report_download_url: Optional[str] = None
    disclaimer: str

class ScreeningHistoryItem(BaseModel):
    id: str
    patient_id: str
    eye: str
    age: Optional[int]
    predicted_stage: str
    predicted_grade: int
    confidence: float
    is_referable: bool
    quality_score: float
    created_at: datetime

    class Config:
        from_attributes = True
