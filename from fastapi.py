from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_and_get_item():
    # 1. إنشاء عنصر جديد
    payload = {"id": 1, "name": "Docker Image"}
    response = client.post("/items", json=payload)
    assert response.status_code == 201
    assert response.json()["item"]["name"] == "Docker Image"

    # 2. قراءة العنصر للتأكد من وجوده
    get_response = client.get("/items/1")
    assert get_response.status_code == 200
    assert get_response.json() == {"id": 1, "name": "Docker Image"}

def test_get_nonexistent_item():
    response = client.get("/items/999")
    assert response.status_code == 404