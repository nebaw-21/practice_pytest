from fastapi import FastAPI, Depends, HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
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

# Test cases
def test_create_item():
    new_item = {"id": 1, "name": "Test Item", "description": "This is a test item."}
    response = client.post("/items", json=new_item)
    assert response.status_code == 200
    assert response.json() == new_item

def test_get_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_update_item():
    updated_item = {"id": 1, "name": "Updated Item", "description": "Updated description."}
    response = client.put("/items/1", json=updated_item)
    assert response.status_code == 200
    assert response.json() == updated_item

# Comment out or remove teardown to keep test.db intact
# def teardown_module():
#     Base.metadata.drop_all(bind=test_engine)