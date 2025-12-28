import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_create_attendance(test_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        event_response = await client.post(
            "/events",
            json={"name": "Test Event", "description": "Test Desc"}
        )
        event_id = event_response.json()["id"]

        candidates_response = await client.put(
            f"/events/{event_id}/candidates",
            json={"candidates": ["Option A"]}
        )
        candidate_id = candidates_response.json()[0]["id"]

        response = await client.post(
            "/attendance",
            json={
                "event_id": event_id,
                "candidate_id": candidate_id,
                "user_id": None,
                "name": "Guest User",
                "comment": "Looking forward!"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Guest User"
        assert data["comment"] == "Looking forward!"
        assert data["candidate_id"] == candidate_id


@pytest.mark.asyncio
async def test_update_attendance(test_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        event_response = await client.post(
            "/events",
            json={"name": "Test Event", "description": "Test Desc"}
        )
        event_id = event_response.json()["id"]

        candidates_response = await client.put(
            f"/events/{event_id}/candidates",
            json={"candidates": ["Option A", "Option B"]}
        )
        candidate_a_id = candidates_response.json()[0]["id"]
        candidate_b_id = candidates_response.json()[1]["id"]

        create_response = await client.post(
            "/attendance",
            json={
                "event_id": event_id,
                "candidate_id": candidate_a_id,
                "user_id": None,
                "name": "Guest",
                "comment": "Original"
            }
        )
        attendance_id = create_response.json()["id"]

        response = await client.put(
            f"/attendance/{attendance_id}",
            json={
                "candidate_id": candidate_b_id,
                "user_id": None,
                "name": "Guest",
                "comment": "Updated"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["candidate_id"] == candidate_b_id
        assert data["comment"] == "Updated"


@pytest.mark.asyncio
async def test_delete_attendance(test_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        event_response = await client.post(
            "/events",
            json={"name": "Test Event", "description": "Test Desc"}
        )
        event_id = event_response.json()["id"]

        candidates_response = await client.put(
            f"/events/{event_id}/candidates",
            json={"candidates": ["Option A"]}
        )
        candidate_id = candidates_response.json()[0]["id"]

        create_response = await client.post(
            "/attendance",
            json={
                "event_id": event_id,
                "candidate_id": candidate_id,
                "user_id": None,
                "name": "Guest",
                "comment": "Test"
            }
        )
        attendance_id = create_response.json()["id"]

        response = await client.delete(f"/attendance/{attendance_id}")
        assert response.status_code == 204


@pytest.mark.asyncio
async def test_list_attendance_by_event(test_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        event_response = await client.post(
            "/events",
            json={"name": "Test Event", "description": "Test Desc"}
        )
        event_id = event_response.json()["id"]

        candidates_response = await client.put(
            f"/events/{event_id}/candidates",
            json={"candidates": ["Option A"]}
        )
        candidate_id = candidates_response.json()[0]["id"]

        await client.post(
            "/attendance",
            json={
                "event_id": event_id,
                "candidate_id": candidate_id,
                "user_id": None,
                "name": "User 1",
                "comment": "C1"
            }
        )
        await client.post(
            "/attendance",
            json={
                "event_id": event_id,
                "candidate_id": candidate_id,
                "user_id": None,
                "name": "User 2",
                "comment": "C2"
            }
        )

        response = await client.get(f"/attendance?event_id={event_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
