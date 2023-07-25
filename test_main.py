from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

jwt_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjYXJsb3MuYS5jdWVydm9AaG90bWFpbC5jb20iLCJleHAiOjE2OTAzMTU0MDF9.MAn5dq8BZCYdPf79HGlWwgUZJf5U8wQPAt75gAvfYik"

def test_create_people():
    test_data = {"id":1, "name": "John Doe", "age": 30}
    response = client.post("/people/", json=test_data, headers={"x-token": jwt_token})
    assert response.status_code == 200
    assert response.json() == test_data

def test_get_people_by_id():
    test_id = 1
    response = client.get(f"/people/{test_id}", headers={"x-token": jwt_token})
    assert response.status_code == 200
    # Assert the response data matches the expected data for that ID

def test_get_people():
    response = client.get("/people/", headers={"x-token": jwt_token})
    assert response.status_code == 200
    # Assert the response data matches the expected data for all people

def test_update_people():
    test_id = 1
    updated_data = {"id": 1, "name": "Updated Name", "age": 25}
    response = client.put(f"/people/{test_id}", json=updated_data, headers={"x-token": jwt_token})
    assert response.status_code == 200
    assert response.json() == updated_data

def test_delete_people():
    test_id = 1
    response = client.delete(f"/people/{test_id}", headers={"x-token": jwt_token})
    assert response.status_code == 204
