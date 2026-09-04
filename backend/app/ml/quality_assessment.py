import numpy as np
from typing import Dict, Any

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    cv2 = None
    CV2_AVAILABLE = False

def assess_retinal_quality(image: np.ndarray) -> Dict[str, Any]:
    """
    Computes clinical Image Quality Assessment (IQA):
    - Sharpness (Laplacian variance / gradient variance)
    - Illumination (Mean gray intensity centering)
    - Contrast (Standard deviation)
    - Usability classification
    """
    if CV2_AVAILABLE:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if image.ndim == 3 else image
        lap_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    else:
        gray = (0.299 * image[:, :, 0] + 0.587 * image[:, :, 1] + 0.114 * image[:, :, 2]).astype(np.float32) if image.ndim == 3 else image.astype(np.float32)
        gy, gx = np.gradient(gray)
        lap_var = float(np.var(gy) + np.var(gx)) * 2.0

    sharpness_score = min(100.0, float(lap_var / 3.0))
    mean_intensity = float(np.mean(gray))
    illumination_score = min(100.0, max(0.0, float(100.0 - abs(mean_intensity - 110.0) * 1.1)))
    std_dev = float(np.std(gray))
    contrast_score = min(100.0, float(std_dev * 1.8))

    overall_score = round(min(100.0, max(0.0, 0.45 * sharpness_score + 0.35 * illumination_score + 0.20 * contrast_score)), 1)
    
    if overall_score >= 60.0:
        status = "Gradable (Optimal for AI)"
        is_gradable = True
    elif overall_score >= 40.0:
        status = "Borderline (Proceed with Caution)"
        is_gradable = True
    else:
        status = "Ungradable (Rescan Recommended)"
        is_gradable = False

    return {
        "overall_quality_score": overall_score,
        "sharpness_score": round(sharpness_score, 1),
        "illumination_score": round(illumination_score, 1),
        "contrast_score": round(contrast_score, 1),
        "status": status,
        "is_gradable": is_gradable
    }
