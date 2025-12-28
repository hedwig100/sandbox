from datetime import datetime
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str


class UserResponse(BaseModel):
    id: str
    name: str
    created_at: datetime
    updated_at: datetime


class EventCreate(BaseModel):
    name: str
    description: str


class EventUpdate(BaseModel):
    name: str
    description: str


class EventResponse(BaseModel):
    id: str
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


class CandidateUpdate(BaseModel):
    candidates: list[str]


class CandidateResponse(BaseModel):
    id: str
    event_id: str
    text: str


class AttendanceCreate(BaseModel):
    event_id: str
    candidate_id: str
    user_id: str | None = None
    name: str
    comment: str


class AttendanceUpdate(BaseModel):
    candidate_id: str
    user_id: str | None = None
    name: str
    comment: str


class AttendanceResponse(BaseModel):
    id: str
    event_id: str
    candidate_id: str
    user_id: str | None
    name: str
    comment: str
