from src.domain.attendance import Attendance
from src.database.connection import get_db


class AttendanceRepository:
    async def create(self, attendance: Attendance) -> Attendance:
        async with get_db() as db:
            await db.execute(
                """
                INSERT INTO attendance (id, event_id, candidate_id, user_id, name, comment)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (attendance.id, attendance.event_id, attendance.candidate_id,
                 attendance.user_id, attendance.name, attendance.comment)
            )
            await db.commit()
            return attendance

    async def update(self, attendance: Attendance) -> Attendance:
        async with get_db() as db:
            await db.execute(
                """
                UPDATE attendance
                SET candidate_id = ?, user_id = ?, name = ?, comment = ?
                WHERE id = ?
                """,
                (attendance.candidate_id, attendance.user_id, attendance.name,
                 attendance.comment, attendance.id)
            )
            await db.commit()
            return attendance

    async def delete(self, attendance_id: str) -> None:
        async with get_db() as db:
            await db.execute(
                "DELETE FROM attendance WHERE id = ?",
                (attendance_id,)
            )
            await db.commit()

    async def find_by_id(self, attendance_id: str) -> Attendance | None:
        async with get_db() as db:
            async with db.execute(
                "SELECT * FROM attendance WHERE id = ?",
                (attendance_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row is None:
                    return None
                return Attendance(
                    id=row["id"],
                    event_id=row["event_id"],
                    candidate_id=row["candidate_id"],
                    user_id=row["user_id"],
                    name=row["name"],
                    comment=row["comment"]
                )

    async def find_by_event_id(self, event_id: str) -> list[Attendance]:
        async with get_db() as db:
            async with db.execute(
                "SELECT * FROM attendance WHERE event_id = ?",
                (event_id,)
            ) as cursor:
                rows = await cursor.fetchall()
                return [
                    Attendance(
                        id=row["id"],
                        event_id=row["event_id"],
                        candidate_id=row["candidate_id"],
                        user_id=row["user_id"],
                        name=row["name"],
                        comment=row["comment"]
                    )
                    for row in rows
                ]
