"""Typed DynamoDB access with Pydantic (schema/validation) + boto3 (I/O).

Design split:
  * Pydantic models  -> the *item* schema: attribute types, required/optional,
    validation, (de)serialization.
  * Repository        -> thin boto3 wrapper that hides the DynamoDB gotchas
    (Decimal vs float, Key building, atomic updates).

The table itself (existence, keys, GSIs, billing) is owned by Terraform; this
module never creates tables. It just reads/writes items.
"""

from __future__ import annotations

import enum
import json
import os
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Generic, Optional, Type, TypeVar

import boto3
from boto3.dynamodb.conditions import Attr
from pydantic import BaseModel, Field

# --- item schemas (Pydantic) -------------------------------------------------


class DynamoItem(BaseModel):
    """Base for every item: a single 'pk' partition key (matches the table)."""

    pk: str


class Visit(DynamoItem):
    pk: str = Field(default_factory=lambda: f"visit#{uuid.uuid4()}")
    ts: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    host: str


class KeyValue(DynamoItem):
    value: str


class Counter(DynamoItem):
    n: int = 0


# A richer item: DynamoDB stores this as a native nested Map, not a JSON blob.
# Nested models -> Map, lists -> List, floats -> Number, enums -> String.
# You can later UpdateItem a single nested path (e.g. "address.city") or
# project just `lines[0].sku` without reading the whole item.


class OrderStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"


class Address(BaseModel):
    city: str
    zip: str
    country: str = "JP"


class LineItem(BaseModel):
    sku: str
    qty: int
    price: float  # declare numbers as float/int so they store as Number, not String


class Order(DynamoItem):
    pk: str = Field(default_factory=lambda: f"order#{uuid.uuid4()}")
    status: OrderStatus = OrderStatus.pending
    customer: str
    address: Address                      # -> nested Map
    lines: list[LineItem] = []            # -> List of Maps
    tags: list[str] = []                  # -> List (use a Python set for a true String Set)
    metadata: dict[str, Any] = {}         # -> open-ended Map (free-form JSON)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def total(self) -> float:
        return sum(li.qty * li.price for li in self.lines)


T = TypeVar("T", bound=DynamoItem)


# --- boto3 <-> python helpers ------------------------------------------------


def _to_dynamo(model: BaseModel) -> dict:
    """Pydantic model -> a dict DynamoDB accepts.

    `mode="json"` makes datetime/UUID/etc. JSON-safe (datetimes become ISO
    strings). The json round-trip with `parse_float=Decimal` then turns every
    float into a Decimal, which is the only numeric type DynamoDB allows.
    """
    raw = model.model_dump(mode="json", exclude_none=True)
    return json.loads(json.dumps(raw), parse_float=Decimal)


# --- repository --------------------------------------------------------------


class Repository(Generic[T]):
    """Typed CRUD over one model. Reads come back as validated `model` objects."""

    def __init__(
        self,
        model: Type[T],
        table_name: Optional[str] = None,
        region: Optional[str] = None,
    ):
        self.model = model
        table_name = table_name or os.environ.get("TABLE_NAME", "dynamodb-sandbox")
        region = region or os.environ.get("AWS_REGION", "ap-northeast-1")
        # On ECS this uses the task role's credentials and travels through the
        # DynamoDB VPC endpoint, so the table's resource policy lets it in.
        self.table = boto3.resource("dynamodb", region_name=region).Table(table_name)

    def put(self, item: T) -> T:
        self.table.put_item(Item=_to_dynamo(item))
        return item

    def get(self, pk: str) -> Optional[T]:
        item = self.table.get_item(Key={"pk": pk}).get("Item")
        return self.model.model_validate(item) if item else None

    def delete(self, pk: str) -> None:
        self.table.delete_item(Key={"pk": pk})

    def list_prefix(self, prefix: str, limit: int = 50) -> list[T]:
        """Items whose pk starts with `prefix`.

        Single-key tables can't Query by partition-key prefix (begins_with is a
        sort-key feature), so this is a filtered Scan -- fine for a sandbox,
        but in real single-table design you'd add a sort key or GSI and Query.
        """
        resp = self.table.scan(
            FilterExpression=Attr("pk").begins_with(prefix), Limit=limit
        )
        return [self.model.model_validate(i) for i in resp.get("Items", [])]

    def add(self, pk: str, attr: str, amount: int = 1) -> int:
        """Atomic counter (ADD). Creates the item if missing."""
        resp = self.table.update_item(
            Key={"pk": pk},
            UpdateExpression="ADD #a :v",
            ExpressionAttributeNames={"#a": attr},
            ExpressionAttributeValues={":v": Decimal(amount)},
            ReturnValues="UPDATED_NEW",
        )
        return int(resp["Attributes"][attr])


# --- demo (run inside ECS, or locally against DynamoDB Local) ----------------

if __name__ == "__main__":
    import socket

    visits = Repository(Visit)
    kv = Repository(KeyValue)
    orders = Repository(Order)

    # write (validated on construction)
    v = visits.put(Visit(host=socket.gethostname()))
    kv.put(KeyValue(pk="greeting", value="hello"))
    total = visits.add("counter#visits", "n")

    # a nested document: stored as a native Map/List, round-trips to a typed object
    o = orders.put(
        Order(
            customer="alice",
            address=Address(city="Tokyo", zip="100-0001"),
            lines=[
                LineItem(sku="A-1", qty=2, price=9.99),
                LineItem(sku="B-7", qty=1, price=120.0),
            ],
            tags=["gift", "priority"],
            metadata={"channel": "web", "coupon": None},
        )
    )

    # read back as typed objects
    print("stored visit:", visits.get(v.pk))
    print("greeting:", kv.get("greeting"))
    print("recent visits:", len(visits.list_prefix("visit#")))
    print("total visits:", total)

    fetched = orders.get(o.pk)
    print("order city:", fetched.address.city)          # nested access
    print("order line 0 sku:", fetched.lines[0].sku)    # list of nested models
    print("order total:", fetched.total)
