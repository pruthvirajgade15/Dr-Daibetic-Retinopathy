import numpy as np
from backend.app.ml.prediction import predict_dr_stage
from backend.app.ml.model import EfficientNetDR

def test_model_instantiation():
    model = EfficientNetDR(num_classes=5, pretrained=False)
    assert model is not None

def test_prediction_output():
    dummy_prep = np.random.randint(40, 220, (224, 224, 3), dtype=np.uint8)
    result = predict_dr_stage(dummy_prep)
    assert "grade" in result
    assert "stage" in result
    assert "confidence" in result
    assert "is_referable" in result
    assert 0 <= result["grade"] <= 4
