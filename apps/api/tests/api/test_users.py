import pytest

@pytest.mark.api
def test_create_user(client):
    resp = client.post("/users/create", json={
        "firstname": "Jane",
        "lastname": "Doe",
        "date_of_birth": "1992-06-15"
    })
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["firstname"] == "Jane"
    # list to confirm presence
    resp2 = client.get("/users")
    assert resp2.status_code == 200
    assert any(d["firstname"] == "Jane" for d in resp2.json())

@pytest.mark.api
def test_list_users(client):
    resp = client.get("/users")
    assert resp.status_code == 200
    arr = resp.json()
    assert isinstance(arr, list)
