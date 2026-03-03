import pytest
import time
from fastapi.testclient import TestClient

def test_fastwq_word(client: TestClient):
    query = "apple"
    response = client.get(f"/fastwq/{query}")
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == query
    assert "ipa_word" in data
    assert "ipa_sentence" in data
    assert "cefr" in data
    assert "frequency" in data
    # apple should have IPA, CEFR and Frequency
    # IPA from en_US.txt uses ɫ instead of l
    assert "/ˈæpəɫ/" in data["ipa_word"]
    assert "ˈæpəɫ" in data["ipa_sentence"]
    assert data["cefr"] == "A1"
    assert float(data["frequency"]) > 0

def test_fastwq_sentence(client: TestClient):
    query = "I ate an apple."
    response = client.get(f"/fastwq/{query}")
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == query
    assert "ipa_word" in data
    assert "ipa_sentence" in data
    # The whole sentence IPA: 'ˈaɪ ˈeɪt ən ˈæpəɫ'
    assert "ˈaɪ ˈeɪt ən ˈæpəɫ" in data["ipa_sentence"]

def test_fastwq_caching(client: TestClient):
    query = "expensive"

    # First call
    start_time = time.time()
    response1 = client.get(f"/fastwq/{query}")
    # duration1 = time.time() - start_time

    # Second call (should be faster due to cache)
    start_time = time.time()
    response2 = client.get(f"/fastwq/{query}")
    # duration2 = time.time() - start_time

    assert response1.json() == response2.json()

def test_fastwq_empty_query(client: TestClient):
    query = " "
    response = client.get(f"/fastwq/{query}")
    assert response.status_code == 200
    data = response.json()
    assert data["cefr"] == "-"
