from fastapi.testclient import TestClient
import importlib


app_module = importlib.import_module("src.app")
app = app_module.app
client = TestClient(app)


def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert "Chess Club" in data


def test_signup_and_duplicate():
    email = "tester@example.com"
    activity = "Chess Club"
    r = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 200
    assert email in r.json()["message"]

    # duplicate signup should fail
    r2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r2.status_code == 400


def test_remove_participant_success_and_not_found():
    activity = "Chess Club"
    email = "to_remove@example.com"
    # sign up then remove
    r = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 200
    r2 = client.delete(
        f"/activities/{activity}/participants", params={"email": email})
    assert r2.status_code == 200

    # removing non-existent participant returns 404
    r3 = client.delete(
        f"/activities/{activity}/participants", params={"email": "noone@example.com"})
    assert r3.status_code == 404
