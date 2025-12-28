from dataclasses import dataclass


@dataclass
class Attendance:
    id: str
    event_id: str
    candidate_id: str
    user_id: str | None
    name: str
    comment: str
