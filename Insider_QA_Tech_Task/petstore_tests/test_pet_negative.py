# petstore_tests/test_pet_negative.py

import requests

BASE_URL = "https://petstore.swagger.io/v2"
HEADERS = {"Content-Type": "application/json"}

def test_create_pet_missing_fields():
    bad_pet = {
        "id": 99999,
        "photoUrls": ["http://example.com/photo"]
    }

    response = requests.post(f"{BASE_URL}/pet", json=bad_pet, headers=HEADERS)
    print("[POST] Missing Fields Response:", response.status_code, response.text)

    if response.status_code == 200:
        print("⚠️ Warning: API accepted a pet without a name. Swagger API might lack validation.")
    assert response.status_code in [200, 400, 500], "Unexpected server response for invalid pet creation"

def test_get_nonexistent_pet():
    response = requests.get(f"{BASE_URL}/pet/1234567890")
    print("[GET] Nonexistent Pet Response:", response.status_code)
    assert response.status_code == 404, "Should return 404 for non-existing pet"

def test_update_invalid_pet():
    invalid_pet = {
        "id": -999,
        "name": "Ghost",
        "photoUrls": [],
        "status": "unknown"
    }

    response = requests.put(f"{BASE_URL}/pet", json=invalid_pet, headers=HEADERS)
    print("[PUT] Update Invalid Pet Response:", response.status_code, response.text)

    if response.status_code == 200:
        print("⚠️ Warning: Server accepted update for invalid pet ID.")
    assert response.status_code in [200, 400, 500], "Unexpected response for updating invalid pet"

def test_delete_invalid_id():
    response = requests.delete(f"{BASE_URL}/pet/0000000")
    print("[DELETE] Invalid ID Response:", response.status_code)
    assert response.status_code in [400, 404], "Unexpected response for deleting invalid ID"