from fastapi import FastAPI, Depends, HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import pytest
from main import app, get_db, Base, ItemModel

# Use SQLite test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Create the test database tables
Base.metadata.create_all(bind=test_engine)

# Override the dependency for testing
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Apply the dependency override
app.dependency_overrides[get_db] = override_get_db

# Create the test client
client = TestClient(app)

# Fixture to reset database before each test
@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield

# Test cases
def test_create_item():
    # Test creating without specifying id (auto-increment)
    new_item = {"name": "Test Item", "description": "This is a test item."}
    response = client.post("/items", json=new_item)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_item["name"]
    assert data["description"] == new_item["description"]
    assert "id" in data
    auto_id = data["id"]



    # Test creating with duplicate id should fail
    duplicate_item = {"id": 2, "name": "Duplicate Item", "description": "This should fail."}
    response = client.post("/items", json=duplicate_item)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_get_items():
    client.post("/items", json={"name": "Test Item", "description": "Test desc"})
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_item():
    create_response = client.post("/items", json={"name": "Test Item", "description": "Test desc"})
    item_id = create_response.json()["id"]
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["id"] == item_id

def test_update_item():
    create_response = client.post("/items", json={"name": "Old Item", "description": "Old desc"})
    item_id = create_response.json()["id"]
    updated_item = {"name": "Updated Item", "description": "Updated description"}
    response = client.put(f"/items/{item_id}", json=updated_item)
    assert response.status_code == 200
    assert response.json() == {**updated_item, "id": item_id}

def test_delete_item():
    create_response = client.post("/items", json={"name": "Test Item", "description": "Test desc"})
    item_id = create_response.json()["id"]
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted successfully"}
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404