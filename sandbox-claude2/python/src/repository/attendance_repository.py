from abc import ABC, abstractmethod
from src.domain.attendance import Attendance


class AttendanceRepository(ABC):
    @abstractmethod
    async def create(self, attendance: Attendance) -> Attendance:
        pass

    @abstractmethod
    async def update(self, attendance: Attendance) -> Attendance:
        pass

    @abstractmethod
    async def delete(self, attendance_id: str) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, attendance_id: str) -> Attendance | None:
        pass

    @abstractmethod
    async def find_by_event_id(self, event_id: str) -> list[Attendance]:
        pass
