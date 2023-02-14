import pytest
from fastapi.testclient import TestClient
from app import app

@pytest.fixture
def client():
    return TestClient(app)

def test_landing(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg":"{{ cookiecutter.project_name }}"}