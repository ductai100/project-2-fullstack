from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from backend.kv_store import get_items, add_item

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/items")
def api_list_items():
    return get_items()

@app.post("/api/items")
def api_add_item(payload: dict = Body(...)):
    text = (payload.get("text") or "").strip()
    if not text:
        return {"error": "text is required"}
    return add_item(text)
