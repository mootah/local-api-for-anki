import json

def test_server_version(client):
    response = client.post("/serverVersion")
    assert response.status_code == 200
    assert "version" in response.json()

def test_yomitan_version(client):
    response = client.post("/yomitanVersion")
    assert response.status_code == 200
    assert "version" in response.json()

def test_tokenize(client):
    payload = {"text": "This is a test.", "scanLength": 20}
    response = client.post("/tokenize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["index"] == 0

    # Verify that reading is populated if a word is in the dictionary
    # 'test' should be in en_US.txt
    test_token = None
    for res in data:
        for content_list in res["content"]:
            for tr in content_list:
                if tr["text"] == "test":
                    test_token = tr
                    break

    if test_token:
        assert test_token["reading"] != ""
        assert "/" not in test_token["reading"]

    # Verify whitespace/punctuation reading is empty
    for res in data:
        for content_list in res["content"]:
            for tr in content_list:
                if tr["text"].strip() == "" or tr["text"] in ".,!":
                    assert tr["reading"] == ""

def test_tokenize_cache(client):
    payload = {"text": "This is a test cache.", "scanLength": 20}

    # First request
    resp1 = client.post("/tokenize", json=payload)
    assert resp1.status_code == 200

    # Second request (should be cached)
    resp2 = client.post("/tokenize", json=payload)
    assert resp2.status_code == 200
    assert resp1.json() == resp2.json()

def test_term_entries(client):
    payload = {"term": "running"}
    response = client.post("/termEntries", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "dictionaryEntries" in data
    assert data["originalTextLength"] == 7
    assert len(data["dictionaryEntries"]) > 0

    entry = data["dictionaryEntries"][0]
    assert entry["headwords"][0]["term"] == "running"

    # Verify reading and pronunciations
    assert entry["headwords"][0]["reading"] != ""
    assert len(entry["pronunciations"]) > 0
    assert "pronunciation" in entry["pronunciations"][0]
    assert "/" not in entry["pronunciations"][0]["pronunciation"]

    # Verify frequencies
    assert len(entry["frequencies"]) > 0
    freq = entry["frequencies"][0]
    assert freq["dictionary"] == "WordFreq"
    assert isinstance(freq["frequency"], (int, float))
    assert freq["frequency"] > 0

def test_term_entries_cache(client):
    payload = {"term": "walking"}

    # First request
    resp1 = client.post("/termEntries", json=payload)
    assert resp1.status_code == 200

    # Second request (should be cached)
    resp2 = client.post("/termEntries", json=payload)
    assert resp2.status_code == 200
    assert resp1.json() == resp2.json()

def test_tokenize_empty_body(client):
    response = client.post("/tokenize")
    assert response.status_code == 422

def test_tokenize_invalid_json(client):
    response = client.post("/tokenize", content="invalid json", headers={"Content-Type": "application/json"})
    assert response.status_code == 422
