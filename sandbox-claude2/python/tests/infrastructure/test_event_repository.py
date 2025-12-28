import pytest
from datetime import datetime
from src.domain.event import Event
from src.infrastructure.event_repository_impl import EventRepositoryImpl


@pytest.mark.asyncio
async def test_create_and_find_event(test_db):
    repository = EventRepositoryImpl()
    now = datetime.now()

    event = Event(
        id="event-1",
        name="Test Event",
        description="Test Description",
        created_at=now,
        updated_at=now
    )

    created_event = await repository.create(event)
    assert created_event.id == "event-1"
    assert created_event.name == "Test Event"

    found_event = await repository.find_by_id("event-1")
    assert found_event is not None
    assert found_event.id == "event-1"
    assert found_event.name == "Test Event"
    assert found_event.description == "Test Description"


@pytest.mark.asyncio
async def test_update_event(test_db):
    repository = EventRepositoryImpl()
    now = datetime.now()

    event = Event(
        id="event-1",
        name="Original Name",
        description="Original Description",
        created_at=now,
        updated_at=now
    )
    await repository.create(event)

    updated_event = Event(
        id="event-1",
        name="Updated Name",
        description="Updated Description",
        created_at=now,
        updated_at=datetime.now()
    )
    result = await repository.update(updated_event)

    assert result.name == "Updated Name"
    assert result.description == "Updated Description"

    found_event = await repository.find_by_id("event-1")
    assert found_event.name == "Updated Name"


@pytest.mark.asyncio
async def test_find_all_events(test_db):
    repository = EventRepositoryImpl()
    now = datetime.now()

    event1 = Event(id="event-1", name="Event 1", description="Desc 1", created_at=now, updated_at=now)
    event2 = Event(id="event-2", name="Event 2", description="Desc 2", created_at=now, updated_at=now)

    await repository.create(event1)
    await repository.create(event2)

    events = await repository.find_all()
    assert len(events) == 2
