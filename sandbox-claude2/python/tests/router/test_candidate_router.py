import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_update_candidates(test_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        event_response = await client.post(
            "/events",
            json={"name": "Test Event", "description": "Test Desc"}
        )
        event_id = event_response.json()["id"]

        response = await client.put(
            f"/events/{event_id}/candidates",
            json={"candidates": ["Option A", "Option B", "Option C"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["text"] == "Option A"
        assert data[1]["text"] == "Option B"
        assert data[2]["text"] == "Option C"


@pytest.mark.asyncio
async def test_list_candidates(test_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        event_response = await client.post(
            "/events",
            json={"name": "Test Event", "description": "Test Desc"}
        )
        event_id = event_response.json()["id"]

        await client.put(
            f"/events/{event_id}/candidates",
            json={"candidates": ["Option A", "Option B"]}
        )

        response = await client.get(f"/events/{event_id}/candidates")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2


@pytest.mark.asyncio
async def test_update_candidates_replaces_existing(test_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        event_response = await client.post(
            "/events",
            json={"name": "Test Event", "description": "Test Desc"}
        )
        event_id = event_response.json()["id"]

        await client.put(
            f"/events/{event_id}/candidates",
            json={"candidates": ["A", "B", "C"]}
        )

        response = await client.put(
            f"/events/{event_id}/candidates",
            json={"candidates": ["X", "Y"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["text"] == "X"
        assert data[1]["text"] == "Y"

        get_response = await client.get(f"/events/{event_id}/candidates")
        assert len(get_response.json()) == 2
