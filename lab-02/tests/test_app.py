import pytest
import app as app_module

@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "COUNTER_FILE", tmp_path / "visits.txt")
    monkeypatch.setattr(app_module, "DATABASE_URL", None)
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as client:
        yield client


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.data == b"ok\n"


def test_ready_file_store(client):
    res = client.get("/ready")
    assert res.status_code == 200
    body = res.get_json()
    assert body["ready"] is True
    assert "file:" in body["store"]


def test_visits_increments(client):
    r1 = client.get("/visits")
    assert r1.status_code == 200
    assert r1.get_json() == {"visits": 1, "store": "file"}

    r2 = client.get("/visits")
    assert r2.status_code == 200
    assert r2.get_json() == {"visits": 2, "store": "file"}


def test_visits_persists_to_file(client, tmp_path):
    client.get("/visits")
    client.get("/visits")
    counter_file = tmp_path / "visits.txt"
    assert counter_file.exists()
    assert counter_file.read_text().strip() == "2"
