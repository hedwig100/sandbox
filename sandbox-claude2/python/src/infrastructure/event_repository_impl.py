from datetime import datetime
from src.domain.event import Event
from src.repository.event_repository import EventRepository
from src.database.connection import get_db


class EventRepositoryImpl(EventRepository):
    async def create(self, event: Event) -> Event:
        async with get_db() as db:
            await db.execute(
                """
                INSERT INTO events (id, name, description, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (event.id, event.name, event.description, event.created_at.isoformat(), event.updated_at.isoformat())
            )
            await db.commit()
            return event

    async def update(self, event: Event) -> Event:
        async with get_db() as db:
            await db.execute(
                """
                UPDATE events
                SET name = ?, description = ?, updated_at = ?
                WHERE id = ?
                """,
                (event.name, event.description, event.updated_at.isoformat(), event.id)
            )
            await db.commit()
            return event

    async def find_by_id(self, event_id: str) -> Event | None:
        async with get_db() as db:
            async with db.execute(
                "SELECT * FROM events WHERE id = ?",
                (event_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row is None:
                    return None
                return Event(
                    id=row["id"],
                    name=row["name"],
                    description=row["description"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                    updated_at=datetime.fromisoformat(row["updated_at"])
                )

    async def find_all(self) -> list[Event]:
        async with get_db() as db:
            async with db.execute("SELECT * FROM events") as cursor:
                rows = await cursor.fetchall()
                return [
                    Event(
                        id=row["id"],
                        name=row["name"],
                        description=row["description"],
                        created_at=datetime.fromisoformat(row["created_at"]),
                        updated_at=datetime.fromisoformat(row["updated_at"])
                    )
                    for row in rows
                ]
