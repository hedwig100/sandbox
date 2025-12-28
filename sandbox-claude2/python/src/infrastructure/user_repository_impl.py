from datetime import datetime
from src.domain.user import User
from src.repository.user_repository import UserRepository
from src.database.connection import get_db


class UserRepositoryImpl(UserRepository):
    async def create(self, user: User) -> User:
        async with get_db() as db:
            await db.execute(
                """
                INSERT INTO users (id, name, created_at, updated_at)
                VALUES (?, ?, ?, ?)
                """,
                (user.id, user.name, user.created_at.isoformat(), user.updated_at.isoformat())
            )
            await db.commit()
            return user

    async def find_by_id(self, user_id: str) -> User | None:
        async with get_db() as db:
            async with db.execute(
                "SELECT * FROM users WHERE id = ?",
                (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row is None:
                    return None
                return User(
                    id=row["id"],
                    name=row["name"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                    updated_at=datetime.fromisoformat(row["updated_at"])
                )

    async def find_all(self) -> list[User]:
        async with get_db() as db:
            async with db.execute("SELECT * FROM users") as cursor:
                rows = await cursor.fetchall()
                return [
                    User(
                        id=row["id"],
                        name=row["name"],
                        created_at=datetime.fromisoformat(row["created_at"]),
                        updated_at=datetime.fromisoformat(row["updated_at"])
                    )
                    for row in rows
                ]
