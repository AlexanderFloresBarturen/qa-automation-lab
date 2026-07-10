def test_get_users_success(client, admin_user, user_payload):
    user_one = user_payload()
    user_two = user_payload()

    created_response_one = client.post("/auth/register", json=user_one)
    created_response_two = client.post("/auth/register", json=user_two)

    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"
    list_response = client.get("/users/", headers=headers)
    list_body = list_response.json()

    assert created_response_one.status_code == 201
    assert created_response_two.status_code == 201
    assert list_response.status_code == 200

    assert isinstance(list_body, list)

    assert len(list_body) == 3


def test_get_users_forbidden(client, loged_user):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    list_response = client.get("/users/", headers=headers)
    list_body = list_response.json()

    assert list_response.status_code == 403

    assert len(list_body) == 1

    assert "detail" in list_body

    assert isinstance(list_body["detail"], str)

    assert list_body["detail"] == "Admin access required"


def test_get_users_without_token(client):
    list_response = client.get("/users", headers={})
    list_body = list_response.json()

    assert list_response.status_code == 401

    assert len(list_body) == 1

    assert "detail" in list_body

    assert isinstance(list_body["detail"], str)

    assert list_body["detail"] == "Not authenticated"


def test_get_users_invalid_token(client):
    headers = {}
    headers["Authorization"] = "Bearer invalid_token"
    list_response = client.get("/users/", headers=headers)
    list_body = list_response.json()

    assert list_response.status_code == 401

    assert len(list_body) == 1

    assert "detail" in list_body

    assert isinstance(list_body["detail"], str)

    assert list_body["detail"] == "Could not validate credentials"
