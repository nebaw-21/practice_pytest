from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

app = FastAPI()

# Define the data model
class Item(BaseModel):
    id: int | None = None  # Optional id, can be specified by client
    name: str
    description: str

# SQLAlchemy setup for real database
SQLALCHEMY_DATABASE_URL = "sqlite:///./real.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ItemModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)  # Auto-increment by default
    name = Column(String, index=True)
    description = Column(String, index=True)

Base.metadata.create_all(bind=engine)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    return db.query(ItemModel).all()

@app.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items")
def create_item(item: Item, db: Session = Depends(get_db)):
    # Check if id is provided and validate uniqueness
    if item.id is not None:
        existing_item = db.query(ItemModel).filter(ItemModel.id == item.id).first()
        if existing_item:
            raise HTTPException(status_code=400, detail=f"Item with id {item.id} already exists")
        db_item = ItemModel(id=item.id, name=item.name, description=item.description)
    else:
        db_item = ItemModel(name=item.name, description=item.description)  # Auto-increment id
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.put("/items/{item_id}")
def update_item(item_id: int, updated_item: Item, db: Session = Depends(get_db)):
    db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = updated_item.name
    db_item.description = updated_item.description
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}