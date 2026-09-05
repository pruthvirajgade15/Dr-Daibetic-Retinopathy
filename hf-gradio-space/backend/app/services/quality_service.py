import numpy as np
from typing import Dict, Any
from ..ml.quality_assessment import assess_retinal_quality

class QualityService:
    @staticmethod
    def evaluate_quality(image: np.ndarray) -> Dict[str, Any]:
        return assess_retinal_quality(image)
