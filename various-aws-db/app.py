"""Tiny web app that reads/writes DynamoDB through the Pydantic + boto3 layer.

Routes:
  GET  /health         -> "ok"
  GET  /               -> record a visit + bump an atomic counter, return total
  GET  /items          -> list recent visit items
  GET  /items/<key>    -> get a KeyValue item
  PUT  /items/<key>    -> body becomes the KeyValue "value" attribute

  POST /orders         -> create an Order from a nested JSON body (validated)
  GET  /orders         -> list orders
  GET  /orders/<id>    -> get one order (id is the uuid part of "order#<id>")

DynamoDB access only works from inside the VPC (through the gateway endpoint),
so this is meant to run on ECS.
"""

import json
import os
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

from pydantic import ValidationError

from dynamo import KeyValue, Order, Repository, Visit

PORT = int(os.environ.get("PORT", "8080"))

visits = Repository(Visit)
kv = Repository(KeyValue)
orders = Repository(Order)

COUNTER_PK = "counter#visits"


def _dump(model) -> dict:
    """Pydantic model -> JSON-safe dict (datetime/enum become strings)."""
    return model.model_dump(mode="json")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self._text(200, "ok")
        elif self.path == "/":
            try:
                visits.put(Visit(host=socket.gethostname()))
                total = visits.add(COUNTER_PK, "n")
                self._text(200, f"Hello from ECS! host={socket.gethostname()} visits={total}")
            except Exception as e:  # don't let a DynamoDB hiccup 500 the page
                self._text(200, f"Hello from ECS! host={socket.gethostname()} db_error={e}")
        elif self.path == "/items":
            self._json(200, [_dump(i) for i in visits.list_prefix("visit#")])
        elif self.path == "/orders":
            self._json(200, [_dump(o) for o in orders.list_prefix("order#")])
        elif self.path.startswith("/orders/"):
            pk = f"order#{self.path[len('/orders/'):]}"
            o = orders.get(pk)
            self._json(200, _dump(o)) if o else self._json(404, {"error": "not found", "pk": pk})
        elif self.path.startswith("/items/"):
            item = kv.get(self.path[len("/items/"):])
            self._json(200, _dump(item)) if item else self._json(404, {"error": "not found"})
        else:
            self._text(404, "not found")

    def do_PUT(self):
        if not self.path.startswith("/items/"):
            self._text(404, "not found")
            return
        key = self.path[len("/items/"):]
        item = kv.put(KeyValue(pk=key, value=self._body()))
        self._json(200, _dump(item))

    def do_POST(self):
        if self.path != "/orders":
            self._text(404, "not found")
            return
        try:
            order = Order(**json.loads(self._body() or "{}"))
        except ValidationError as e:  # schema validation failed -> 400 with details
            self._json(400, {"error": "validation", "detail": json.loads(e.json())})
            return
        except json.JSONDecodeError:
            self._json(400, {"error": "invalid json"})
            return
        orders.put(order)
        self._json(201, _dump(order) | {"total": order.total})

    def _body(self) -> str:
        length = int(self.headers.get("Content-Length", "0"))
        return self.rfile.read(length).decode() if length else ""

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
    print(f"listening on :{PORT}", flush=True)
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
