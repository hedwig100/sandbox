import aiosqlite
from contextlib import asynccontextmanager


DATABASE_PATH = "app.db"


@asynccontextmanager
async def get_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        yield db


async def init_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                id TEXT PRIMARY KEY,
                event_id TEXT NOT NULL,
                text TEXT NOT NULL,
                FOREIGN KEY (event_id) REFERENCES events(id)
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id TEXT PRIMARY KEY,
                event_id TEXT NOT NULL,
                candidate_id TEXT NOT NULL,
                user_id TEXT,
                name TEXT NOT NULL,
                comment TEXT NOT NULL,
                FOREIGN KEY (event_id) REFERENCES events(id),
                FOREIGN KEY (candidate_id) REFERENCES candidates(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        await db.commit()
