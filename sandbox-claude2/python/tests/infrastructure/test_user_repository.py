import pytest
from datetime import datetime
from src.domain.user import User
from src.infrastructure.user_repository_impl import UserRepositoryImpl


@pytest.mark.asyncio
async def test_create_and_find_user(test_db):
    repository = UserRepositoryImpl()
    now = datetime.now()

    user = User(
        id="user-1",
        name="Test User",
        created_at=now,
        updated_at=now
    )

    created_user = await repository.create(user)
    assert created_user.id == "user-1"
    assert created_user.name == "Test User"

    found_user = await repository.find_by_id("user-1")
    assert found_user is not None
    assert found_user.id == "user-1"
    assert found_user.name == "Test User"


@pytest.mark.asyncio
async def test_find_all_users(test_db):
    repository = UserRepositoryImpl()
    now = datetime.now()

    user1 = User(id="user-1", name="User 1", created_at=now, updated_at=now)
    user2 = User(id="user-2", name="User 2", created_at=now, updated_at=now)

    await repository.create(user1)
    await repository.create(user2)

    users = await repository.find_all()
    assert len(users) == 2


@pytest.mark.asyncio
async def test_find_nonexistent_user(test_db):
    repository = UserRepositoryImpl()

    found_user = await repository.find_by_id("nonexistent")
    assert found_user is None
