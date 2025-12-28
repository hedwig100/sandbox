import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_create_user(test_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/users",
            json={"name": "Test User"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test User"
        assert "id" in data
        assert "created_at" in data


@pytest.mark.asyncio
async def test_list_users(test_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post("/users", json={"name": "User 1"})
        await client.post("/users", json={"name": "User 2"})

        response = await client.get("/users")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2


@pytest.mark.asyncio
async def test_get_user(test_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        create_response = await client.post("/users", json={"name": "Test User"})
        user_id = create_response.json()["id"]

        response = await client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["name"] == "Test User"


@pytest.mark.asyncio
async def test_get_nonexistent_user(test_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/users/nonexistent")
        assert response.status_code == 404
