# api/items.py
from http.server import BaseHTTPRequestHandler
import json
import os

DATA_FILE = "/tmp/items.json"

def load_items():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_items(items):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        items = load_items()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(items).encode())

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        data = json.loads(body.decode())

        items = load_items()
        items.append(data)
        save_items(items)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True}).encode())
