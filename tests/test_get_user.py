def test_get_user_success(client, created_user):
    response = client.get(f"/users/{created_user['id']}")
    body = response.json()

    assert response.status_code == 200

    assert len(body) == 4

    assert "id" in body
    assert "name" in body
    assert "email" in body
    assert "age" in body

    assert isinstance(body["id"], int)
    assert isinstance(body["name"], str)
    assert isinstance(body["email"], str)
    assert isinstance(body["age"], int)

    assert body["id"] > 0

    assert body["id"] == created_user["id"]
    assert body["name"] == created_user["name"]
    assert body["email"] == created_user["email"]
    assert body["age"] == created_user["age"]

def test_get_user_not_found(client):
    response = client.get("/users/9999")
    body = response.json()

    assert response.status_code == 404

    assert len(body) == 1

    assert "detail" in body

    assert isinstance(body["detail"], str)

    assert body["detail"] == "User not found"