import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional

def generate_session_token() -> str:
    return secrets.token_urlsafe(32)

def hash_patient_identifier(patient_id: str) -> str:
    """Anonymizes patient ID for HIPAA / GDPR compliant logging."""
    return hashlib.sha256(patient_id.strip().upper().encode()).hexdigest()[:16]
