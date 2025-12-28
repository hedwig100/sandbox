from uuid import uuid4
from fastapi import APIRouter, HTTPException
from src.domain.candidate import Candidate
from src.infrastructure.candidate_repository_impl import CandidateRepositoryImpl
from src.infrastructure.event_repository_impl import EventRepositoryImpl
from src.router.schemas import CandidateUpdate, CandidateResponse


router = APIRouter(prefix="/events/{event_id}/candidates", tags=["candidates"])
candidate_repository = CandidateRepositoryImpl()
event_repository = EventRepositoryImpl()


@router.put("", response_model=list[CandidateResponse])
async def update_candidates(event_id: str, candidate_data: CandidateUpdate):
    event = await event_repository.find_by_id(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    await candidate_repository.delete_by_event_id(event_id)

    candidates = []
    for text in candidate_data.candidates:
        candidate = Candidate(
            id=str(uuid4()),
            event_id=event_id,
            text=text
        )
        created_candidate = await candidate_repository.create(candidate)
        candidates.append(created_candidate)

    return [
        CandidateResponse(
            id=candidate.id,
            event_id=candidate.event_id,
            text=candidate.text
        )
        for candidate in candidates
    ]


@router.get("", response_model=list[CandidateResponse])
async def list_candidates(event_id: str):
    event = await event_repository.find_by_id(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    candidates = await candidate_repository.find_by_event_id(event_id)
    return [
        CandidateResponse(
            id=candidate.id,
            event_id=candidate.event_id,
            text=candidate.text
        )
        for candidate in candidates
    ]
