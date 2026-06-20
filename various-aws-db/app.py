"""Tiny dependency-light web app that plays with DynamoDB via boto3.

Routes:
  GET  /health        -> "ok"
  GET  /              -> records a visit + bumps an atomic counter, returns the total
  GET  /items         -> lists the most recent visit items (Scan)
  PUT  /items/<key>   -> body becomes the item's "value" attribute (PutItem)
  GET  /items/<key>   -> returns one item (GetItem)

DynamoDB access only works from inside the VPC (through the gateway endpoint)
because of the table's resource policy -- so this is meant to run on ECS.
"""

import json
import os
import socket
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer

import boto3
from boto3.dynamodb.conditions import Key  # noqa: F401  (handy when extending)

PORT = int(os.environ.get("PORT", "8080"))
TABLE_NAME = os.environ.get("TABLE_NAME", "dynamodb-sandbox")
REGION = os.environ.get("AWS_REGION", "ap-northeast-1")

_table = boto3.resource("dynamodb", region_name=REGION).Table(TABLE_NAME)

COUNTER_PK = "counter#visits"
VISIT_PREFIX = "visit#"


def record_visit():
    """Store one visit item and atomically bump the running total."""
    now = datetime.now(timezone.utc).isoformat()
    _table.put_item(
        Item={"pk": f"{VISIT_PREFIX}{uuid.uuid4()}", "ts": now, "host": socket.gethostname()}
    )
    resp = _table.update_item(
        Key={"pk": COUNTER_PK},
        UpdateExpression="ADD #n :one",
        ExpressionAttributeNames={"#n": "n"},
        ExpressionAttributeValues={":one": 1},
        ReturnValues="UPDATED_NEW",
    )
    return int(resp["Attributes"]["n"])


def list_items(limit=20):
    items = _table.scan(Limit=limit).get("Items", [])
    # DynamoDB Decimals aren't JSON-serializable; stringify defensively.
    return json.loads(json.dumps(items, default=str))


def put_item(key, value):
    _table.put_item(Item={"pk": key, "value": value})


def get_item(key):
    return _table.get_item(Key={"pk": key}).get("Item")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self._text(200, "ok")
        elif self.path == "/":
            try:
                total = record_visit()
                self._text(200, f"Hello from ECS! host={socket.gethostname()} visits={total}")
            except Exception as e:  # don't let a DynamoDB hiccup 500 the page
                self._text(200, f"Hello from ECS! host={socket.gethostname()} db_error={e}")
        elif self.path == "/items":
            self._json(200, list_items())
        elif self.path.startswith("/items/"):
            key = self.path[len("/items/"):]
            item = get_item(key)
            if item is None:
                self._json(404, {"error": "not found", "pk": key})
            else:
                self._json(200, json.loads(json.dumps(item, default=str)))
        else:
            self._text(404, "not found")

    def do_PUT(self):
        if not self.path.startswith("/items/"):
            self._text(404, "not found")
            return
        key = self.path[len("/items/"):]
        length = int(self.headers.get("Content-Length", "0"))
        value = self.rfile.read(length).decode() if length else ""
        put_item(key, value)
        self._json(200, {"pk": key, "value": value})

    def _text(self, code, body):
        self._send(code, "text/plain; charset=utf-8", body + "\n")

    def _json(self, code, obj):
        self._send(code, "application/json", json.dumps(obj, ensure_ascii=False) + "\n")

    def _send(self, code, content_type, body):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} - {fmt % args}", flush=True)


if __name__ == "__main__":
    print(f"table={TABLE_NAME} region={REGION}", flush=True)
    print(f"listening on :{PORT}", flush=True)
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
