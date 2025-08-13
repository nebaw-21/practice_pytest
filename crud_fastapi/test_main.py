from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_item():
    new_item = {"id": 1, "name": "Test Item", "description": "This is a test item."}
    response = client.post("/items", json=new_item)
    assert response.status_code == 200
    assert response.json() == new_item

def test_get_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_update_item():
    updated_item = {"id": 1, "name": "Updated Item", "description": "Updated description."}
    response = client.put("/items/1", json=updated_item)
    assert response.status_code == 200
    assert response.json() == updated_item

def test_delete_item():
    response = client.delete("/items/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
