from datetime import datetime
from dataclasses import dataclass


@dataclass
class Event:
    id: str
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
