# petstore_tests/test_pet_crud.py

import random
import time
import requests

BASE_URL = "https://petstore.swagger.io/v2"
HEADERS = {"Content-Type": "application/json"}

def retry_request(method, url, expected_status=200, retries=3, delay=1, **kwargs):
    """Generic retry wrapper for requests."""
    for attempt in range(retries):
        response = requests.request(method, url, **kwargs)
        if response.status_code == expected_status:
            return response
        time.sleep(delay)
    return response  # Last response after retries

def test_crud_pet_lifecycle():
    random_id = random.randint(10000, 99999)
    new_pet = {
        "id": random_id,
        "name": "Buddy",
        "photoUrls": ["http://example.com/photo"],
        "status": "available"
    }

    # Step 1: Create a new pet (POST)
    response = requests.post(f"{BASE_URL}/pet", json=new_pet, headers=HEADERS)
    print("[POST] Create Pet Response:", response.status_code, response.text)
    assert response.status_code == 200, "Failed to create pet"
    assert response.json().get("name") == "Buddy"

    # Step 2: Get the pet (GET) with retries
    response = retry_request("GET", f"{BASE_URL}/pet/{random_id}", expected_status=200)
    print("[GET] Fetch Pet Response:", response.status_code, response.text)
    assert response.status_code == 200, "Failed to fetch pet after creation"

    # Step 3: Update the pet (PUT) with retries
    updated_pet = new_pet.copy()
    updated_pet["name"] = "BuddyUpdated"
    updated_pet["status"] = "sold"

    response = retry_request(
        "PUT", f"{BASE_URL}/pet",
        expected_status=200,
        json=updated_pet, headers=HEADERS
    )
    print("[PUT] Update Pet Response:", response.status_code, response.text)
    assert response.json().get("name") == "BuddyUpdated"

    # Step 4: Delete the pet (DELETE) with retries
    response = retry_request("DELETE", f"{BASE_URL}/pet/{random_id}", expected_status=200)
    print("[DELETE] Delete Pet Response:", response.status_code, response.text)

    # Step 5: Verify deletion (GET should return 404)
    response = retry_request("GET", f"{BASE_URL}/pet/{random_id}", expected_status=404)
    print("[GET] After Deletion Response:", response.status_code, response.text)
    assert response.status_code == 404, "Pet was not deleted properly"