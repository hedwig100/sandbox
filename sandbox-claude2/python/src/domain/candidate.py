from dataclasses import dataclass


@dataclass
class Candidate:
    id: str
    event_id: str
    text: str
