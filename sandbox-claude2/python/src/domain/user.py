from datetime import datetime
from dataclasses import dataclass


@dataclass
class User:
    id: str
    name: str
    created_at: datetime
    updated_at: datetime
