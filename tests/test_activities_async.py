import importlib
import pytest
from httpx import AsyncClient, ASGITransport


app = importlib.import_module("src.app").app


@pytest.mark.asyncio
async def test_get_activities_async():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get("/activities")
    assert r.status_code == 200
    assert "Chess Club" in r.json()


@pytest.mark.asyncio
async def test_signup_and_duplicate_async():
    activity = "Chess Club"
    email = "async@example.com"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.post(f"/activities/{activity}/signup", params={"email": email})
        assert r.status_code == 200
        r2 = await ac.post(f"/activities/{activity}/signup", params={"email": email})
        assert r2.status_code == 400


@pytest.mark.asyncio
async def test_remove_participant_async():
    activity = "Chess Club"
    email = "async-remove@example.com"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post(f"/activities/{activity}/signup", params={"email": email})
        r = await ac.delete(f"/activities/{activity}/participants", params={"email": email})
    assert r.status_code == 200
