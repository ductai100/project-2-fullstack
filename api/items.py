from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import uuid

app = FastAPI()

# CORS (để frontend gọi được)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "data.json"

class Item(BaseModel):
    text: str

def read_db():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def write_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# GET
@app.get("/api/items")
def get_items():
    return read_db()

# POST
@app.post("/api/items")
def add_item(item: Item):
    data = read_db()
    new_item = {
        "id": str(uuid.uuid4()),
        "text": item.text
    }
    data.append(new_item)
    write_db(data)
    return new_item

# DELETE ⭐
@app.delete("/api/items/{item_id}")
def delete_item(item_id: str):
    data = read_db()
    new_data = [i for i in data if i["id"] != item_id]
    write_db(new_data)
    return {"ok": True}
