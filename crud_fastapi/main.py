from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

# Define the data model
class Item(BaseModel):
    id: int
    name: str
    description: str

# In-memory database (local file storage)
DB_FILE = "database.json"

def read_database():
    try:
        with open(DB_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def write_database(data):
    with open(DB_FILE, "w") as file:
        json.dump(data, file)

@app.get("/items")
def get_items():
    return read_database()

@app.get("/items/{item_id}")
def get_item(item_id: int):
    items = read_database()
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items")
def create_item(item: Item):
    items = read_database()
    if any(existing_item["id"] == item.id for existing_item in items):
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items.append(item.model_dump())
    write_database(items)
    return item

@app.put("/items/{item_id}")
def update_item(item_id: int, updated_item: Item):
    items = read_database()
    for index, item in enumerate(items):
        if item["id"] == item_id:
            items[index] = updated_item.model_dump()
            write_database(items)
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    items = read_database()
    for index, item in enumerate(items):
        if item["id"] == item_id:
            deleted_item = items.pop(index)
            write_database(items)
            return deleted_item
    raise HTTPException(status_code=404, detail="Item not found")
