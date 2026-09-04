import numpy as np
from PIL import Image, ImageFilter, ImageOps
from typing import Tuple

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    cv2 = None
    CV2_AVAILABLE = False

def crop_fundus_borders(image: np.ndarray, tol: int = 10) -> np.ndarray:
    """Crops empty black outer borders."""
    if image.ndim == 2:
        mask = image > tol
        return image[np.ix_(mask.any(1), mask.any(0))]
    elif image.ndim == 3:
        if CV2_AVAILABLE:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = (0.299 * image[:, :, 0] + 0.587 * image[:, :, 1] + 0.114 * image[:, :, 2]).astype(np.uint8)
        mask = gray > tol
        if image[:, :, 0][np.ix_(mask.any(1), mask.any(0))].shape[0] == 0:
            return image
        img1 = image[:, :, 0][np.ix_(mask.any(1), mask.any(0))]
        img2 = image[:, :, 1][np.ix_(mask.any(1), mask.any(0))]
        img3 = image[:, :, 2][np.ix_(mask.any(1), mask.any(0))]
        return np.stack([img1, img2, img3], axis=-1)
    return image

def ben_graham_preprocess(image: np.ndarray, image_size: int = 224, sigma: float = 10.0) -> np.ndarray:
    """
    Ben Graham color standardization:
    - Crops black borders
    - Rescales to square
    - Blurs and subtracts: 4*img - 4*Gaussian(img) + 128
    """
    cropped = crop_fundus_borders(image, tol=10)
    if cropped.shape[0] < 20 or cropped.shape[1] < 20:
        cropped = image

    if CV2_AVAILABLE:
        resized = cv2.resize(cropped, (image_size, image_size), interpolation=cv2.INTER_AREA)
        blurred = cv2.GaussianBlur(resized, (0, 0), sigmaX=sigma)
        enhanced = cv2.addWeighted(resized, 4.0, blurred, -4.0, 128)
        
        mask = np.zeros((image_size, image_size), dtype=np.uint8)
        center = (image_size // 2, image_size // 2)
        radius = int(image_size * 0.48)
        cv2.circle(mask, center, radius, 255, -1)
        enhanced = cv2.bitwise_and(enhanced, enhanced, mask=mask)
        return enhanced
    else:
        pil_img = Image.fromarray(cropped).resize((image_size, image_size), Image.Resampling.BILINEAR)
        pil_blurred = pil_img.filter(ImageFilter.GaussianBlur(radius=sigma / 2.0))
        img_np = np.array(pil_img, dtype=np.float32)
        blur_np = np.array(pil_blurred, dtype=np.float32)
        enhanced = 4.0 * img_np - 4.0 * blur_np + 128.0
        enhanced = np.clip(enhanced, 0, 255).astype(np.uint8)
        
        y, x = np.ogrid[:image_size, :image_size]
        cx, cy = image_size // 2, image_size // 2
        mask = ((x - cx)**2 + (y - cy)**2) <= (image_size * 0.48)**2
        enhanced[~mask] = 0
        return enhanced

def segment_vessels_and_disc(image: np.ndarray) -> np.ndarray:
    """Creates a multi-structure overlay highlighting vessels (Cyan) and optic disc (Amber)."""
    h, w = image.shape[:2]
    green = image[:, :, 1] if image.ndim == 3 else image
    red = image[:, :, 0] if image.ndim == 3 else image
    
    if CV2_AVAILABLE:
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        enh_green = clahe.apply(green)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        tophat = cv2.morphologyEx(enh_green, cv2.MORPH_TOPHAT, kernel)
        blackhat = cv2.morphologyEx(enh_green, cv2.MORPH_BLACKHAT, kernel)
        vessels_raw = cv2.subtract(cv2.add(enh_green, tophat), blackhat)
        vessel_mask = cv2.adaptiveThreshold(vessels_raw, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 3)
        
        # Optic Disc
        blurred_red = cv2.GaussianBlur(red, (15, 15), 0)
        _, _, _, max_loc = cv2.minMaxLoc(blurred_red)
        cx, cy = max_loc
    else:
        pil_green = Image.fromarray(green)
        edges = pil_green.filter(ImageFilter.FIND_EDGES)
        edge_np = np.array(edges)
        vessel_mask = (edge_np > np.percentile(edge_np, 85)).astype(np.uint8) * 255
        
        pil_red = Image.fromarray(red).filter(ImageFilter.GaussianBlur(radius=7))
        red_blur = np.array(pil_red)
        cy, cx = np.unravel_index(np.argmax(red_blur), red_blur.shape)

    radius = int(min(h, w) * 0.08)
    overlay = image.copy()
    overlay[vessel_mask > 0] = [0, 220, 255] # Cyan vessels
    
    y, x = np.ogrid[:h, :w]
    od_mask = ((x - cx)**2 + (y - cy)**2) <= radius**2
    overlay[od_mask] = [255, 200, 0] # Amber Optic Disc
    
    return (image.astype(np.float32) * 0.60 + overlay.astype(np.float32) * 0.40).astype(np.uint8)
