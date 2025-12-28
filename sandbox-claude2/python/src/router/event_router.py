from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, HTTPException
from src.domain.event import Event
from src.repository.event_repository import EventRepository
from src.router.schemas import EventCreate, EventUpdate, EventResponse


router = APIRouter(prefix="/events", tags=["events"])
event_repository = EventRepository()


@router.post("", response_model=EventResponse, status_code=201)
async def create_event(event_data: EventCreate):
    now = datetime.now()
    event = Event(
        id=str(uuid4()),
        name=event_data.name,
        description=event_data.description,
        created_at=now,
        updated_at=now
    )
    created_event = await event_repository.create(event)
    return EventResponse(
        id=created_event.id,
        name=created_event.name,
        description=created_event.description,
        created_at=created_event.created_at,
        updated_at=created_event.updated_at
    )


@router.put("/{event_id}", response_model=EventResponse)
async def update_event(event_id: str, event_data: EventUpdate):
    existing_event = await event_repository.find_by_id(event_id)
    if existing_event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    updated_event = Event(
        id=event_id,
        name=event_data.name,
        description=event_data.description,
        created_at=existing_event.created_at,
        updated_at=datetime.now()
    )
    result = await event_repository.update(updated_event)
    return EventResponse(
        id=result.id,
        name=result.name,
        description=result.description,
        created_at=result.created_at,
        updated_at=result.updated_at
    )


@router.get("", response_model=list[EventResponse])
async def list_events():
    events = await event_repository.find_all()
    return [
        EventResponse(
            id=event.id,
            name=event.name,
            description=event.description,
            created_at=event.created_at,
            updated_at=event.updated_at
        )
        for event in events
    ]


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: str):
    event = await event_repository.find_by_id(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventResponse(
        id=event.id,
        name=event.name,
        description=event.description,
        created_at=event.created_at,
        updated_at=event.updated_at
    )
