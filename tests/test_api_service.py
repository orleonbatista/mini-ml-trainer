
import pytest
from fastapi.testclient import TestClient
from ..api_service.main import app

client = TestClient(app)

def test_root_status():
    response = client.get("/")
    assert response.status_code == 200
    assert "API Front ativa!" in response.json()["message"]

def test_train_invalid_file_type():
    response = client.post(
        "/train",
        files={"dataset_file": ("test.txt", "some content")},
        data={
            "model_type": "RandomForestClassifier",
            "model_params": "{}",
            "target_column": "target"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Apenas arquivos CSV são suportados."

def test_predict_invalid_file_type():
    response = client.post(
        "/predict",
        files={"input_file": ("test.txt", "some content")},
        data={"columns_to_drop": None}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Apenas arquivos CSV são suportados."

# Add more tests as needed for different scenarios