import io
from typing import Optional, List
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from PIL import Image
import numpy as np

from ...schemas.screening import ScreeningResponse
from ...services.screening_service import ScreeningService
from ...api.dependencies import get_database_session

router = APIRouter()

@router.post("/screen", response_model=ScreeningResponse)
async def screen_retinal_image(
    file: UploadFile = File(...),
    patient_id: str = Form("PATIENT_01"),
    eye: str = Form("OD"),
    age: Optional[int] = Form(None),
    db: Session = Depends(get_database_session)
):
    """
    Primary endpoint: processes uploaded fundus photography through IQA, Ben Graham, PyTorch DR model, and Grad-CAM.
    """
    try:
        content = await file.read()
        pil_img = Image.open(io.BytesIO(content)).convert("RGB")
        image_np = np.array(pil_img)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {e}")

    result = ScreeningService.process_screening(
        image_np=image_np,
        patient_id=patient_id,
        eye=eye,
        age=age,
        db=db
    )
    return result
