import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_create_event(test_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/events",
            json={"name": "Test Event", "description": "Test Description"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Event"
        assert data["description"] == "Test Description"
        assert "id" in data


@pytest.mark.asyncio
async def test_update_event(test_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        create_response = await client.post(
            "/events",
            json={"name": "Original", "description": "Original Desc"}
        )
        event_id = create_response.json()["id"]

        response = await client.put(
            f"/events/{event_id}",
            json={"name": "Updated", "description": "Updated Desc"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated"
        assert data["description"] == "Updated Desc"


@pytest.mark.asyncio
async def test_list_events(test_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post("/events", json={"name": "Event 1", "description": "Desc 1"})
        await client.post("/events", json={"name": "Event 2", "description": "Desc 2"})

        response = await client.get("/events")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2


@pytest.mark.asyncio
async def test_get_event(test_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        create_response = await client.post(
            "/events",
            json={"name": "Test Event", "description": "Test Desc"}
        )
        event_id = create_response.json()["id"]

        response = await client.get(f"/events/{event_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == event_id
        assert data["name"] == "Test Event"
