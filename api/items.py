from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json
import os

app = FastAPI()

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

# GET all
@app.get("/api/items")
def get_items():
    return read_db()

# ADD
@app.post("/api/items")
def add_item(item: Item):
    data = read_db()
    data.append(item.text)
    write_db(data)
    return {"ok": True}

# DELETE (theo index)
@app.delete("/api/items/{index}")
def delete_item(index: int):
    data = read_db()
    if index < 0 or index >= len(data):
        return {"error": "Invalid index"}
    data.pop(index)
    write_db(data)
    return {"ok": True}
