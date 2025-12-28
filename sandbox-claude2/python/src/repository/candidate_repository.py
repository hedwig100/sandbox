from abc import ABC, abstractmethod
from src.domain.candidate import Candidate


class CandidateRepository(ABC):
    @abstractmethod
    async def create(self, candidate: Candidate) -> Candidate:
        pass

    @abstractmethod
    async def update(self, candidate: Candidate) -> Candidate:
        pass

    @abstractmethod
    async def find_by_id(self, candidate_id: str) -> Candidate | None:
        pass

    @abstractmethod
    async def find_by_event_id(self, event_id: str) -> list[Candidate]:
        pass

    @abstractmethod
    async def delete_by_event_id(self, event_id: str) -> None:
        pass
