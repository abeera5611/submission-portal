import pytest
from app import create_app

@pytest.fixture
def client(tmp_path):
    return create_app(str(tmp_path / "s.json")).test_client()

GOOD = {"name": "Ali", "reg_no": "FA22-001", "title": "Lab 1", "url": "https://example.com/a"}

def test_valid_submission_saved_and_listed(client):
    r = client.post("/", data=GOOD)
    assert b"Lab 1" in client.get("/").data

def test_missing_registration_number_rejected(client):
    r = client.post("/", data={**GOOD, "reg_no": ""})
    assert b"reg_no is required" in r.data
    assert b"Lab 1" not in client.get("/").data

def test_invalid_url_rejected(client):
    r = client.post("/", data={**GOOD, "url": "not-a-url"})
    assert b"Invalid submission URL" in r.data
    assert b"Lab 1" not in client.get("/").data