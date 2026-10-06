from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="DevOps Demo App", version="1.0.0")

# Database شيك بسيطة في الذاكرة
db: Dict[int, str] = {}

class Item(BaseModel):
    id: int
    name: str

@app.get("/")
def read_root():
    return {"status": "success", "message": "DevOps Pipeline Demo API is running!"}

@app.get("/health")
def health_check():
    # يُستخدم للـ Kubernetes Readiness / Liveness Probes
    return {"status": "healthy"}

@app.post("/items", status_code=201)
def create_item(item: Item):
    if item.id in db:
        raise HTTPException(status_code=400, detail="Item already exists")
    db[item.id] = item.name
    return {"message": "Item created successfully", "item": item}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, "name": db[item_id]}