import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from ..ml.preprocessing import ben_graham_preprocess, segment_vessels_and_disc
from ..ml.quality_assessment import assess_retinal_quality
from ..ml.prediction import predict_dr_stage
from ..ml.gradcam import generate_gradcam_overlay
from ..utils.image_utils import np_to_base64
from ..database import crud
from ..core.config import settings
from .report_service import ReportService

class ScreeningService:
    @staticmethod
    def process_screening(
        image_np: Any,
        patient_id: str,
        eye: str = "OD",
        age: Optional[int] = None,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        screening_id = str(uuid.uuid4())

        # 1. Quality Assessment
        quality = assess_retinal_quality(image_np)

        # 2. Ben Graham Preprocessing
        preprocessed = ben_graham_preprocess(image_np, image_size=224)

        # 3. Model Prediction
        prediction = predict_dr_stage(preprocessed)

        # 4. Grad-CAM Explainability & Structure Segmentation
        gradcam_img, explainability = generate_gradcam_overlay(image_np, prediction["grade"])
        structures_img = segment_vessels_and_disc(image_np)

        raw_images = {
            "original": image_np,
            "preprocessed": preprocessed,
            "gradcam": gradcam_img,
            "structures": structures_img
        }

        # 5. Generate Clinical Reports
        report_files = ReportService.generate_report(
            screening_id=screening_id,
            patient_id=patient_id,
            eye=eye,
            prediction=prediction,
            quality=quality,
            explainability=explainability,
            images_dict=raw_images
        )

        # 6. Save to Database if session provided
        if db is not None:
            try:
                crud.create_screening_record(db, {
                    "id": screening_id,
                    "patient_id": patient_id,
                    "eye": eye,
                    "age": age,
                    "quality_score": quality["overall_quality_score"],
                    "is_gradable": quality["is_gradable"],
                    "quality_status": quality["status"],
                    "predicted_grade": prediction["grade"],
                    "predicted_stage": prediction["stage"],
                    "confidence": prediction["confidence"],
                    "is_referable": prediction["is_referable"],
                    "clinical_urgency": prediction["clinical_urgency"],
                    "probabilities": prediction["probabilities"],
                    "dominant_quadrant": explainability["dominant_quadrant"],
                    "quadrant_distribution": explainability["quadrants"],
                    "report_html_path": report_files["html_path"],
                    "report_txt_path": report_files["txt_path"],
                })
            except Exception as e:
                print(f"[!] Warning: Failed saving to database: {e}")

        return {
            "id": screening_id,
            "status": "success",
            "patient_id": patient_id,
            "eye": eye,
            "age": age,
            "created_at": datetime.utcnow().isoformat(),
            "quality": quality,
            "prediction": prediction,
            "explainability": explainability,
            "images": {
                "original": np_to_base64(image_np),
                "preprocessed": np_to_base64(preprocessed),
                "gradcam": np_to_base64(gradcam_img),
                "structures": np_to_base64(structures_img),
            },
            "report_download_url": f"/reports/{report_files['html_filename']}",
            "disclaimer": settings.MEDICAL_DISCLAIMER
        }
