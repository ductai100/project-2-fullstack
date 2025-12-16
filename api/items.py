from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json, uuid, os
import urllib.request

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

KV_URL = os.getenv("KV_REST_API_URL", "").rstrip("/")
KV_TOKEN = os.getenv("KV_REST_API_TOKEN", "")

KEY = "project2_items"

class ItemIn(BaseModel):
    text: str

def kv_request(method: str, path: str, body: dict | None = None):
    if not KV_URL or not KV_TOKEN:
        raise RuntimeError("Missing KV_REST_API_URL or KV_REST_API_TOKEN in Vercel env")

    url = f"{KV_URL}{path}"
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {KV_TOKEN}")
    req.add_header("Content-Type", "application/json")

    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def get_items():
    # Upstash REST: GET /get/<key>
    r = kv_request("GET", f"/get/{KEY}")
    raw = r.get("result")
    if not raw:
        return []
    try:
        return json.loads(raw)
    except:
        return []

def set_items(items):
    # Upstash REST: POST /set/<key>  {"value":"..."}
    kv_request("POST", f"/set/{KEY}", {"value": json.dumps(items, ensure_ascii=False)})

@app.get("/api/items")
def api_get():
    return get_items()

@app.post("/api/items")
def api_add(item: ItemIn):
    items = get_items()
    new_item = {"id": str(uuid.uuid4()), "text": item.text}
    items.append(new_item)
    set_items(items)
    return new_item

@app.delete("/api/items/{item_id}")
def api_delete(item_id: str):
    items = get_items()
    items = [x for x in items if x.get("id") != item_id]
    set_items(items)
    return {"ok": True}
