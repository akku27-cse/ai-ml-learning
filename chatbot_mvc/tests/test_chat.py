from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_chat_route():
    response = client.post("/api/chat", json={"user_id": "test", "message": "When should I vaccinate a puppy?"})
    assert response.status_code == 200
    assert "reply" in response.json()