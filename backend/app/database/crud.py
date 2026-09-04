from typing import List, Optional
from sqlalchemy.orm import Session
from .models import ScreeningRecord

def create_screening_record(db: Session, record_data: dict) -> ScreeningRecord:
    db_record = ScreeningRecord(**record_data)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_screening_record(db: Session, screening_id: str) -> Optional[ScreeningRecord]:
    return db.query(ScreeningRecord).filter(ScreeningRecord.id == screening_id).first()

def get_all_screenings(db: Session, skip: int = 0, limit: int = 100) -> List[ScreeningRecord]:
    return db.query(ScreeningRecord).order_by(ScreeningRecord.created_at.desc()).offset(skip).limit(limit).all()

def get_screenings_by_patient(db: Session, patient_id: str) -> List[ScreeningRecord]:
    return db.query(ScreeningRecord).filter(ScreeningRecord.patient_id == patient_id).order_by(ScreeningRecord.created_at.desc()).all()
