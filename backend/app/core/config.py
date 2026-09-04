import os
from pathlib import Path
from typing import List

class Settings:
    PROJECT_NAME: str = "DR-Screening-AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = "supersecretclinickeyfordiabeticretinopathyscreening"
    
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    MODEL_PATH: Path = BASE_DIR / "models" / "efficientnet_dr.pth"
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    REPORTS_DIR: Path = BASE_DIR / "reports"
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'screening.db'}"
    
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]
    
    MEDICAL_DISCLAIMER: str = (
        "This system is an AI-assisted screening tool and does not replace "
        "professional ophthalmic examination and clinical diagnosis."
    )

settings = Settings()

# Ensure runtime directories exist
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
settings.MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
