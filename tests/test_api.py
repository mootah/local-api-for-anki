import httpx
import time

BASE_URL = "http://127.0.0.1:19634"

def test_tokenize_cache():
    payload = {"text": "This is a test.", "scanLength": 20}

    # First request
    start = time.time()
    resp1 = httpx.post(f"{BASE_URL}/tokenize", json=payload)
    end1 = time.time() - start
    assert resp1.status_code == 200

    # Second request (should be cached)
    start = time.time()
    resp2 = httpx.post(f"{BASE_URL}/tokenize", json=payload)
    end2 = time.time() - start
    assert resp2.status_code == 200
    assert resp1.json() == resp2.json()

    print(f"Tokenize: 1st={end1:.4f}s, 2rd={end2:.4f}s")

def test_term_entries_cache():
    payload = {"term": "running"}

    # First request
    start = time.time()
    resp1 = httpx.post(f"{BASE_URL}/termEntries", json=payload)
    end1 = time.time() - start
    assert resp1.status_code == 200

    # Second request (should be cached)
    start = time.time()
    resp2 = httpx.post(f"{BASE_URL}/termEntries", json=payload)
    end2 = time.time() - start
    assert resp2.status_code == 200
    assert resp1.json() == resp2.json()

    print(f"TermEntries: 1st={end1:.4f}s, 2rd={end2:.4f}s")

if __name__ == "__main__":
    try:
        test_tokenize_cache()
        test_term_entries_cache()
        print("All tests passed!")
    except Exception as e:
        print(f"Test failed: {e}")
        exit(1)

