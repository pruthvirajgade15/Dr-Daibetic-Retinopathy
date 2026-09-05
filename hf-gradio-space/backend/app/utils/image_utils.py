import io
import base64
import numpy as np
from PIL import Image

def np_to_base64(image_np: np.ndarray, format: str = "PNG") -> str:
    """Converts a numpy RGB image array to base64 Data URL."""
    if image_np is None:
        return ""
    if image_np.dtype != np.uint8:
        image_np = np.clip(image_np, 0, 255).astype(np.uint8)
    
    pil_img = Image.fromarray(image_np)
    buffer = io.BytesIO()
    pil_img.save(buffer, format=format)
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/{format.lower()};base64,{encoded}"

def bytes_to_numpy(image_bytes: bytes) -> np.ndarray:
    """Reads raw bytes into an RGB numpy array."""
    pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return np.array(pil_img)
