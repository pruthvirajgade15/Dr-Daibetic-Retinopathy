import io
import numpy as np
from PIL import Image
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_screen_flow():
    img = Image.fromarray(np.random.randint(50, 200, (224, 224, 3), dtype=np.uint8))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    response = client.post(
        "/api/screen",
        files={"file": ("fundus_test.png", buf, "image/png")},
        data={"patient_id": "TEST_PAT_01", "eye": "OD", "age": 60}
    )
    assert response.status_code == 200
    res = response.json()
    assert res["status"] == "success"
    assert "quality" in res
    assert "prediction" in res
    assert "explainability" in res
    assert "images" in res

def test_history_flow():
    response = client.get("/api/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
