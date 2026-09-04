import numpy as np
from backend.app.ml.quality_assessment import assess_retinal_quality

def test_assess_quality():
    dummy_img = np.random.randint(30, 200, (224, 224, 3), dtype=np.uint8)
    q = assess_retinal_quality(dummy_img)
    assert "overall_quality_score" in q
    assert "sharpness_score" in q
    assert "status" in q
    assert "is_gradable" in q
    assert 0.0 <= q["overall_quality_score"] <= 100.0
