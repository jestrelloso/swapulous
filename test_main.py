from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_all_reviews():
    response = client.get("/review")
    assert response.status_code == 200