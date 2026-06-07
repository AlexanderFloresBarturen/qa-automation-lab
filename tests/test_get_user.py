def test_get_user_success(client, valid_user_payload):
    create_response = client.post("/users", json=valid_user_payload)
    body_post = create_response.json()

    get_response = client.get(f"/users/{body_post['id']}")
    body_get = get_response.json()

    assert get_response.status_code == 200

    assert len(body_get) == 4

    assert "id" in body_get
    assert "name" in body_get
    assert "email" in body_get
    assert "age" in body_get

    assert isinstance(body_get["id"], int)
    assert isinstance(body_get["name"], str)
    assert isinstance(body_get["email"], str)
    assert isinstance(body_get["age"], int)

    assert body_get["id"] > 0

    assert body_get["id"] == body_post["id"]
    assert body_get["name"] == body_post["name"]
    assert body_get["email"] == body_post["email"]
    assert body_get["age"] == body_post["age"]

def test_get_user_not_found(client):
    response = client.get("/users/0")
    body = response.json()

    assert response.status_code == 404

    assert len(body) == 1

    assert "detail" in body

    assert isinstance(body["detail"], str)

    assert body["detail"] == "User not found"