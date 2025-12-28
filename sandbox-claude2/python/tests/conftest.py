import pytest
import os
import aiosqlite
from src.database.connection import init_db, DATABASE_PATH


@pytest.fixture
async def test_db():
    test_db_path = "test_app.db"
    original_db_path = DATABASE_PATH

    import src.database.connection as db_module
    db_module.DATABASE_PATH = test_db_path

    await init_db()

    yield

    db_module.DATABASE_PATH = original_db_path

    if os.path.exists(test_db_path):
        os.remove(test_db_path)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"
