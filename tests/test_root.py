from fastapi.testclient import TestClient
import importlib


app = importlib.import_module("src.app").app
client = TestClient(app)


def test_root_redirect():
    r = client.get("/", follow_redirects=False)
    assert r.status_code in (301, 302, 307, 308)
    assert r.headers["location"] == "/static/index.html"
