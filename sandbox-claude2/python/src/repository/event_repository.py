from abc import ABC, abstractmethod
from src.domain.event import Event


class EventRepository(ABC):
    @abstractmethod
    async def create(self, event: Event) -> Event:
        pass

    @abstractmethod
    async def update(self, event: Event) -> Event:
        pass

    @abstractmethod
    async def find_by_id(self, event_id: str) -> Event | None:
        pass

    @abstractmethod
    async def find_all(self) -> list[Event]:
        pass
