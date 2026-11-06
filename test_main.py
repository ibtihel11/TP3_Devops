from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_subtract():
    response = client.get("/subtract", params={"a": 10, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"result": 7}