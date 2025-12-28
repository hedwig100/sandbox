from abc import ABC, abstractmethod
from src.domain.user import User


class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def find_by_id(self, user_id: str) -> User | None:
        pass

    @abstractmethod
    async def find_all(self) -> list[User]:
        pass
