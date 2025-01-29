import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
# from api_service.main import app
from api_service.main import app

client = TestClient(app)

def test_root_status():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "ok"}
        mock_get.return_value = mock_response

        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "API Front ativa!"

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

def test_train_success():
    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "training started"}
        mock_post.return_value = mock_response

        with open("test.csv", "w") as f:
            f.write("col1,col2,target\n1,2,0\n3,4,1")

        with open("test.csv", "rb") as f:
            response = client.post(
                "/train",
                files={"dataset_file": ("test.csv", f)},
                data={
                    "model_type": "RandomForestClassifier",
                    "model_params": "{}",
                    "target_column": "target"
                }
            )
        assert response.status_code == 200
        assert response.json()["status"] == "training started"

def test_predict_invalid_file_type():
    response = client.post(
        "/predict",
        files={"input_file": ("test.txt", "some content")},
        data={"columns_to_drop": None}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Apenas arquivos CSV são suportados."

def test_predict_success():
    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"predictions": [0, 1]}
        mock_post.return_value = mock_response

        with open("test.csv", "w") as f:
            f.write("col1,col2\n1,2\n3,4")

        with open("test.csv", "rb") as f:
            response = client.post(
                "/predict",
                files={"input_file": ("test.csv", f)},
                data={"columns_to_drop": None}
            )
        assert response.status_code == 200
        assert response.json()["predictions"] == [0, 1]