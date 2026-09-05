from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...schemas.screening import ScreeningHistoryItem
from ...database import crud
from ...api.dependencies import get_database_session

router = APIRouter()

@router.get("/history", response_model=List[ScreeningHistoryItem])
async def list_screenings(skip: int = 0, limit: int = 50, db: Session = Depends(get_database_session)):
    """Fetches historical clinical screening records."""
    records = crud.get_all_screenings(db, skip=skip, limit=limit)
    return records

@router.get("/history/{screening_id}", response_model=ScreeningHistoryItem)
async def get_screening(screening_id: str, db: Session = Depends(get_database_session)):
    record = crud.get_screening_record(db, screening_id)
    if not record:
        raise HTTPException(status_code=404, detail="Screening record not found.")
    return record
