def test_update_user_success(client, created_user, valid_update_payload):
    update_response = client.put(f"/users/{created_user['id']}", json=valid_update_payload)
    body_update = update_response.json()

    get_response = client.get(f"/users/{created_user['id']}")
    body_get = get_response.json()

    assert update_response.status_code == 200
    assert get_response.status_code == 200

    assert len(body_update) == 4

    assert "id" in body_update
    assert "name" in body_update
    assert "email" in body_update
    assert "age" in body_update

    assert isinstance(body_update["id"], int)
    assert isinstance(body_update["name"], str)
    assert isinstance(body_update["email"], str)
    assert isinstance(body_update["age"], int)

    assert body_update["id"] > 0

    assert body_update["id"] == created_user["id"]

    assert body_update["name"] == valid_update_payload["name"]
    assert body_update["email"] == valid_update_payload["email"]
    assert body_update["age"] == valid_update_payload["age"]

    # Se verifica que los cambios se han reflejado en la DB
    assert body_get["name"] == valid_update_payload["name"]
    assert body_get["email"] == valid_update_payload["email"]
    assert body_get["age"] == valid_update_payload["age"]

def test_update_user_not_found(client, valid_update_payload):
    response = client.put(f"/users/{9999}", json=valid_update_payload)
    body = response.json()

    assert response.status_code == 404

    assert len(body) == 1

    assert "detail" in body

    assert body["detail"] == "User not found"

def test_update_user_duplicate_email(client, user_payload, valid_update_payload):
    user_first = user_payload()
    user_second = user_payload()

    post_response_first = client.post("/users", json=user_first)

    post_response_second = client.post("/users", json=user_second)
    body_post_second = post_response_second.json()

    update_payload = valid_update_payload.copy()
    update_payload["email"] = user_first["email"]
    print(f"Second: {body_post_second}")
    put_response = client.put(f"/users/{body_post_second['id']}", json=update_payload)
    body_put = put_response.json()

    assert put_response.status_code == 409

    assert len(body_put) == 1

    assert "detail" in body_put

    assert body_put["detail"] == "Email already exists"

def test_update_deleted_user(client, created_user, valid_update_payload):
    delete_response = client.delete(f"/users/{created_user['id']}")

    update_response = client.put(f"/users/{created_user['id']}", json=valid_update_payload)
    body_update = update_response.json()

    assert update_response.status_code == 404

    assert len(body_update) == 1

    assert "detail" in body_update

    assert body_update["detail"] == "User not found"

