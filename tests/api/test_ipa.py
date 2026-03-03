import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ipa_search():
    response = client.get("/ipa/search", params={"q": "^appl"})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) > 0
    assert any(r["word"] == "apple" for r in data["results"])

def test_ipa_crud():
    word = "testword456"
    ipa = "test-ipa"

    # Create
    response = client.post("/ipa/", json={"word": word, "ipa": ipa})
    assert response.status_code == 200

    # Create existing
    response = client.post("/ipa/", json={"word": word, "ipa": ipa})
    assert response.status_code == 400

    # Update
    new_ipa = "updated-ipa"
    response = client.put(f"/ipa/{word}", json={"ipa": new_ipa})
    assert response.status_code == 200
    assert response.json()["ipa"] == new_ipa

    # Search for it
    response = client.get("/ipa/search", params={"q": f"^{word}$"})
    assert response.status_code == 200
    assert response.json()["results"][0]["ipa"] == new_ipa

    # Get single word
    response = client.get(f"/ipa/{word}")
    assert response.status_code == 200
    assert response.json()["ipa"] == new_ipa

    # Delete
    response = client.delete(f"/ipa/{word}")
    assert response.status_code == 200

    # Search again
    response = client.get("/ipa/search", params={"q": f"^{word}$"})
    assert response.status_code == 200
    assert response.json()["total"] == 0


def test_ipa_get_word():
    # Existing word
    response = client.get("/ipa/apple")
    assert response.status_code == 200
    assert response.json()["word"] == "apple"

    # Case insensitive
    response = client.get("/ipa/APPLE")
    assert response.status_code == 200
    assert response.json()["word"] == "apple"

    # Non-existing word
    response = client.get("/ipa/nonexistentword123")
    assert response.status_code == 404
