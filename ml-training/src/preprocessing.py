import cv2
import numpy as np
from PIL import Image

def ben_graham_clahe(image_np: np.ndarray, image_size: int = 224, sigma: float = 10.0) -> np.ndarray:
    """
    Ben Graham Color Standardization + Circular Retinal Masking.
    """
    h, w = image_np.shape[:2]
    resized = cv2.resize(image_np, (image_size, image_size), interpolation=cv2.INTER_AREA)
    blurred = cv2.GaussianBlur(resized, (0, 0), sigmaX=sigma)
    enhanced = cv2.addWeighted(resized, 4.0, blurred, -4.0, 128)

    mask = np.zeros((image_size, image_size), dtype=np.uint8)
    center = (image_size // 2, image_size // 2)
    radius = int(image_size * 0.48)
    cv2.circle(mask, center, radius, 255, -1)
    return cv2.bitwise_and(enhanced, enhanced, mask=mask)
