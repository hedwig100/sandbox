from uuid import uuid4
from fastapi import APIRouter, HTTPException
from src.domain.attendance import Attendance
from src.infrastructure.attendance_repository_impl import AttendanceRepositoryImpl
from src.infrastructure.event_repository_impl import EventRepositoryImpl
from src.infrastructure.candidate_repository_impl import CandidateRepositoryImpl
from src.router.schemas import AttendanceCreate, AttendanceUpdate, AttendanceResponse


router = APIRouter(prefix="/attendance", tags=["attendance"])
attendance_repository = AttendanceRepositoryImpl()
event_repository = EventRepositoryImpl()
candidate_repository = CandidateRepositoryImpl()


@router.post("", response_model=AttendanceResponse, status_code=201)
async def create_attendance(attendance_data: AttendanceCreate):
    event = await event_repository.find_by_id(attendance_data.event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    candidate = await candidate_repository.find_by_id(attendance_data.candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")

    attendance = Attendance(
        id=str(uuid4()),
        event_id=attendance_data.event_id,
        candidate_id=attendance_data.candidate_id,
        user_id=attendance_data.user_id,
        name=attendance_data.name,
        comment=attendance_data.comment
    )
    created_attendance = await attendance_repository.create(attendance)
    return AttendanceResponse(
        id=created_attendance.id,
        event_id=created_attendance.event_id,
        candidate_id=created_attendance.candidate_id,
        user_id=created_attendance.user_id,
        name=created_attendance.name,
        comment=created_attendance.comment
    )


@router.put("/{attendance_id}", response_model=AttendanceResponse)
async def update_attendance(attendance_id: str, attendance_data: AttendanceUpdate):
    existing_attendance = await attendance_repository.find_by_id(attendance_id)
    if existing_attendance is None:
        raise HTTPException(status_code=404, detail="Attendance not found")

    candidate = await candidate_repository.find_by_id(attendance_data.candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")

    updated_attendance = Attendance(
        id=attendance_id,
        event_id=existing_attendance.event_id,
        candidate_id=attendance_data.candidate_id,
        user_id=attendance_data.user_id,
        name=attendance_data.name,
        comment=attendance_data.comment
    )
    result = await attendance_repository.update(updated_attendance)
    return AttendanceResponse(
        id=result.id,
        event_id=result.event_id,
        candidate_id=result.candidate_id,
        user_id=result.user_id,
        name=result.name,
        comment=result.comment
    )


@router.delete("/{attendance_id}", status_code=204)
async def delete_attendance(attendance_id: str):
    existing_attendance = await attendance_repository.find_by_id(attendance_id)
    if existing_attendance is None:
        raise HTTPException(status_code=404, detail="Attendance not found")

    await attendance_repository.delete(attendance_id)


@router.get("", response_model=list[AttendanceResponse])
async def list_attendance_by_event(event_id: str):
    event = await event_repository.find_by_id(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    attendances = await attendance_repository.find_by_event_id(event_id)
    return [
        AttendanceResponse(
            id=attendance.id,
            event_id=attendance.event_id,
            candidate_id=attendance.candidate_id,
            user_id=attendance.user_id,
            name=attendance.name,
            comment=attendance.comment
        )
        for attendance in attendances
    ]
