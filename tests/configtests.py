import pytest
from fastapi.testclient import TestClient
from app.main import app  # Import the FastAPI app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
