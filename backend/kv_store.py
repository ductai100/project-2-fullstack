import os, json, requests

KV_URL = os.getenv("KV_REST_API_URL")
KV_TOKEN = os.getenv("KV_REST_API_TOKEN")

KEY = "project2:items"

def _headers():
    return {
        "Authorization": f"Bearer {KV_TOKEN}",
        "Content-Type": "application/json",
    }

def get_items():
    # GET {KV_URL}/get/{KEY}
    r = requests.get(f"{KV_URL}/get/{KEY}", headers=_headers(), timeout=20)
    r.raise_for_status()
    data = r.json()
    raw = data.get("result")
    return json.loads(raw) if raw else []

def set_items(items):
    # POST {KV_URL}/set/{KEY}  body: {"value":"..."}
    payload = {"value": json.dumps(items, ensure_ascii=False)}
    r = requests.post(f"{KV_URL}/set/{KEY}", headers=_headers(), data=json.dumps(payload), timeout=20)
    r.raise_for_status()

def add_item(text: str):
    items = get_items()
    new_id = (items[0]["id"] + 1) if items else 1
    item = {"id": new_id, "text": text}
    items.insert(0, item)
    set_items(items)
    return item
