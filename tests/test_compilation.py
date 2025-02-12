from fastapi.testclient import TestClient
from src.compilation import app

client = TestClient(app)

def test_webhook_invalid_payload():
    response = client.post("/webhook", json={})
    assert response.status_code == 400
    assert "Invalid payload" in response.json()["detail"]

def test_webhook_valid_branch():
    response = client.post("/webhook", json={"ref": "refs/heads/test-branch"})
    assert response.status_code == 200
    assert "Compilation (syntax check) completed" in response.json()["message"]
