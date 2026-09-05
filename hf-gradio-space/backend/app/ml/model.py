import os
import torch
import torch.nn as nn
from typing import Optional
from ..core.config import settings

try:
    import torchvision.models as tv_models
    TV_AVAILABLE = True
except ImportError:
    TV_AVAILABLE = False

class DRClassificationHead(nn.Module):
    def __init__(self, in_features: int, num_classes: int = 5, dropout_rate: float = 0.3):
        super().__init__()
        self.head = nn.Sequential(
            nn.Linear(in_features, 512),
            nn.LayerNorm(512),
            nn.SiLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(512, 128),
            nn.LayerNorm(128),
            nn.SiLU(),
            nn.Dropout(dropout_rate / 2.0),
            nn.Linear(128, num_classes)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.head(x)

class EfficientNetDR(nn.Module):
    def __init__(self, model_name: str = "efficientnet_b0", num_classes: int = 5, pretrained: bool = False, dropout_rate: float = 0.3):
        super().__init__()
        if not TV_AVAILABLE:
            raise ImportError("torchvision is required for EfficientNetDR.")
        weights = tv_models.EfficientNet_B0_Weights.DEFAULT if pretrained else None
        self.backbone = tv_models.efficientnet_b0(weights=weights)
        in_features = self.backbone.classifier[1].in_features
        self.backbone.classifier = DRClassificationHead(in_features, num_classes, dropout_rate)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.backbone(x)

    def get_last_conv_layer(self):
        return self.backbone.features[-1]

_GLOBAL_MODEL: Optional[EfficientNetDR] = None

def load_dr_model(weights_path: Optional[str] = None) -> Optional[EfficientNetDR]:
    global _GLOBAL_MODEL
    if _GLOBAL_MODEL is not None:
        return _GLOBAL_MODEL

    path = weights_path or str(settings.MODEL_PATH)
    if os.path.exists(path):
        try:
            model = EfficientNetDR(num_classes=5, pretrained=False)
            checkpoint = torch.load(path, map_location="cpu")
            state_dict = checkpoint.get("model_state_dict", checkpoint)
            model.load_state_dict(state_dict)
            model.eval()
            _GLOBAL_MODEL = model
            print(f"[+] Loaded deep learning model from {path}")
            return _GLOBAL_MODEL
        except Exception as e:
            print(f"[!] Warning: Failed loading model weights from {path}: {e}")
            return None
    return None
