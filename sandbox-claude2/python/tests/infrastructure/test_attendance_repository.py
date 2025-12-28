import pytest
from datetime import datetime
from src.domain.event import Event
from src.domain.candidate import Candidate
from src.domain.attendance import Attendance
from src.infrastructure.event_repository_impl import EventRepositoryImpl
from src.infrastructure.candidate_repository_impl import CandidateRepositoryImpl
from src.infrastructure.attendance_repository_impl import AttendanceRepositoryImpl


@pytest.mark.asyncio
async def test_create_and_find_attendance(test_db):
    event_repo = EventRepositoryImpl()
    candidate_repo = CandidateRepositoryImpl()
    attendance_repo = AttendanceRepositoryImpl()
    now = datetime.now()

    event = Event(id="event-1", name="Event", description="Desc", created_at=now, updated_at=now)
    await event_repo.create(event)

    candidate = Candidate(id="cand-1", event_id="event-1", text="Option A")
    await candidate_repo.create(candidate)

    attendance = Attendance(
        id="att-1",
        event_id="event-1",
        candidate_id="cand-1",
        user_id=None,
        name="Guest User",
        comment="Looking forward to it"
    )
    created_attendance = await attendance_repo.create(attendance)

    assert created_attendance.id == "att-1"
    assert created_attendance.name == "Guest User"

    found_attendance = await attendance_repo.find_by_id("att-1")
    assert found_attendance is not None
    assert found_attendance.comment == "Looking forward to it"


@pytest.mark.asyncio
async def test_update_attendance(test_db):
    event_repo = EventRepositoryImpl()
    candidate_repo = CandidateRepositoryImpl()
    attendance_repo = AttendanceRepositoryImpl()
    now = datetime.now()

    event = Event(id="event-1", name="Event", description="Desc", created_at=now, updated_at=now)
    await event_repo.create(event)

    cand1 = Candidate(id="cand-1", event_id="event-1", text="Option A")
    cand2 = Candidate(id="cand-2", event_id="event-1", text="Option B")
    await candidate_repo.create(cand1)
    await candidate_repo.create(cand2)

    attendance = Attendance(
        id="att-1",
        event_id="event-1",
        candidate_id="cand-1",
        user_id=None,
        name="Guest",
        comment="Original"
    )
    await attendance_repo.create(attendance)

    updated_attendance = Attendance(
        id="att-1",
        event_id="event-1",
        candidate_id="cand-2",
        user_id=None,
        name="Guest",
        comment="Updated"
    )
    result = await attendance_repo.update(updated_attendance)

    assert result.candidate_id == "cand-2"
    assert result.comment == "Updated"


@pytest.mark.asyncio
async def test_delete_attendance(test_db):
    event_repo = EventRepositoryImpl()
    candidate_repo = CandidateRepositoryImpl()
    attendance_repo = AttendanceRepositoryImpl()
    now = datetime.now()

    event = Event(id="event-1", name="Event", description="Desc", created_at=now, updated_at=now)
    await event_repo.create(event)

    candidate = Candidate(id="cand-1", event_id="event-1", text="Option A")
    await candidate_repo.create(candidate)

    attendance = Attendance(
        id="att-1",
        event_id="event-1",
        candidate_id="cand-1",
        user_id=None,
        name="Guest",
        comment="Test"
    )
    await attendance_repo.create(attendance)

    await attendance_repo.delete("att-1")

    found_attendance = await attendance_repo.find_by_id("att-1")
    assert found_attendance is None


@pytest.mark.asyncio
async def test_find_by_event_id(test_db):
    event_repo = EventRepositoryImpl()
    candidate_repo = CandidateRepositoryImpl()
    attendance_repo = AttendanceRepositoryImpl()
    now = datetime.now()

    event = Event(id="event-1", name="Event", description="Desc", created_at=now, updated_at=now)
    await event_repo.create(event)

    candidate = Candidate(id="cand-1", event_id="event-1", text="Option A")
    await candidate_repo.create(candidate)

    att1 = Attendance(id="att-1", event_id="event-1", candidate_id="cand-1", user_id=None, name="User1", comment="C1")
    att2 = Attendance(id="att-2", event_id="event-1", candidate_id="cand-1", user_id=None, name="User2", comment="C2")
    await attendance_repo.create(att1)
    await attendance_repo.create(att2)

    attendances = await attendance_repo.find_by_event_id("event-1")
    assert len(attendances) == 2
