from src.domain.candidate import Candidate
from src.database.connection import get_db


class CandidateRepository:
    async def create(self, candidate: Candidate) -> Candidate:
        async with get_db() as db:
            await db.execute(
                """
                INSERT INTO candidates (id, event_id, text)
                VALUES (?, ?, ?)
                """,
                (candidate.id, candidate.event_id, candidate.text)
            )
            await db.commit()
            return candidate

    async def update(self, candidate: Candidate) -> Candidate:
        async with get_db() as db:
            await db.execute(
                """
                UPDATE candidates
                SET text = ?
                WHERE id = ?
                """,
                (candidate.text, candidate.id)
            )
            await db.commit()
            return candidate

    async def find_by_id(self, candidate_id: str) -> Candidate | None:
        async with get_db() as db:
            async with db.execute(
                "SELECT * FROM candidates WHERE id = ?",
                (candidate_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row is None:
                    return None
                return Candidate(
                    id=row["id"],
                    event_id=row["event_id"],
                    text=row["text"]
                )

    async def find_by_event_id(self, event_id: str) -> list[Candidate]:
        async with get_db() as db:
            async with db.execute(
                "SELECT * FROM candidates WHERE event_id = ?",
                (event_id,)
            ) as cursor:
                rows = await cursor.fetchall()
                return [
                    Candidate(
                        id=row["id"],
                        event_id=row["event_id"],
                        text=row["text"]
                    )
                    for row in rows
                ]

    async def delete_by_event_id(self, event_id: str) -> None:
        async with get_db() as db:
            await db.execute(
                "DELETE FROM candidates WHERE event_id = ?",
                (event_id,)
            )
            await db.commit()
