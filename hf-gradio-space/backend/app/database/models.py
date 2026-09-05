import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, JSON
from .database import Base

class ScreeningRecord(Base):
    __tablename__ = "screenings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(64), index=True, nullable=False)
    patient_hash = Column(String(64), nullable=True)
    eye = Column(String(4), default="OD") # OD (Right), OS (Left)
    age = Column(Integer, nullable=True)
    
    # Image Quality
    quality_score = Column(Float, nullable=False)
    is_gradable = Column(Boolean, default=True)
    quality_status = Column(String(64), nullable=False)
    
    # Diagnosis Prediction
    predicted_grade = Column(Integer, nullable=False) # 0 to 4
    predicted_stage = Column(String(64), nullable=False) # No DR, Mild, etc.
    confidence = Column(Float, nullable=False)
    is_referable = Column(Boolean, default=False)
    clinical_urgency = Column(String(128), nullable=False)
    probabilities = Column(JSON, nullable=True)
    
    # Explainability & Visuals
    dominant_quadrant = Column(String(64), nullable=True)
    quadrant_distribution = Column(JSON, nullable=True)
    
    # File Paths
    original_image_path = Column(String(256), nullable=True)
    report_html_path = Column(String(256), nullable=True)
    report_txt_path = Column(String(256), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
