import pytest
from datetime import datetime
from src.domain.event import Event
from src.domain.candidate import Candidate
from src.infrastructure.event_repository_impl import EventRepositoryImpl
from src.infrastructure.candidate_repository_impl import CandidateRepositoryImpl


@pytest.mark.asyncio
async def test_create_and_find_candidate(test_db):
    event_repo = EventRepositoryImpl()
    candidate_repo = CandidateRepositoryImpl()
    now = datetime.now()

    event = Event(id="event-1", name="Event", description="Desc", created_at=now, updated_at=now)
    await event_repo.create(event)

    candidate = Candidate(id="cand-1", event_id="event-1", text="Option A")
    created_candidate = await candidate_repo.create(candidate)

    assert created_candidate.id == "cand-1"
    assert created_candidate.text == "Option A"

    found_candidate = await candidate_repo.find_by_id("cand-1")
    assert found_candidate is not None
    assert found_candidate.text == "Option A"


@pytest.mark.asyncio
async def test_find_by_event_id(test_db):
    event_repo = EventRepositoryImpl()
    candidate_repo = CandidateRepositoryImpl()
    now = datetime.now()

    event = Event(id="event-1", name="Event", description="Desc", created_at=now, updated_at=now)
    await event_repo.create(event)

    cand1 = Candidate(id="cand-1", event_id="event-1", text="Option A")
    cand2 = Candidate(id="cand-2", event_id="event-1", text="Option B")
    await candidate_repo.create(cand1)
    await candidate_repo.create(cand2)

    candidates = await candidate_repo.find_by_event_id("event-1")
    assert len(candidates) == 2


@pytest.mark.asyncio
async def test_delete_by_event_id(test_db):
    event_repo = EventRepositoryImpl()
    candidate_repo = CandidateRepositoryImpl()
    now = datetime.now()

    event = Event(id="event-1", name="Event", description="Desc", created_at=now, updated_at=now)
    await event_repo.create(event)

    cand1 = Candidate(id="cand-1", event_id="event-1", text="Option A")
    cand2 = Candidate(id="cand-2", event_id="event-1", text="Option B")
    await candidate_repo.create(cand1)
    await candidate_repo.create(cand2)

    await candidate_repo.delete_by_event_id("event-1")

    candidates = await candidate_repo.find_by_event_id("event-1")
    assert len(candidates) == 0
