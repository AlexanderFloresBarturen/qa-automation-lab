from tests.helpers import assert_valid_user_response_admin, assert_user_not_found_response

def test_get_user_success(client, admin_user, user_payload):
    user_one = user_payload()

    created_response = client.post("/auth/register", json=user_one)
    created_body = created_response.json()

    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"
    get_response = client.get(f"/users/{created_body["id"]}", headers=headers)
    get_body = get_response.json()

    assert created_response.status_code == 201
    assert get_response.status_code == 200

    assert_valid_user_response_admin(get_body)

    assert get_body["id"] == created_body["id"]
    assert get_body["name"] == created_body["name"]
    assert get_body["email"] == created_body["email"]
    assert get_body["age"] == created_body["age"]

def test_get_user_nonexisting_user(client, admin_user):
    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"
    get_response = client.get("/users/99999", headers=headers)
    get_body = get_response.json()

    assert get_response.status_code == 404

    assert_user_not_found_response(get_body)

def test_get_user_forbidden(client, loged_user, user_payload):
    user_one = user_payload()

    created_response = client.post("/auth/register", json=user_one)
    created_body = created_response.json()

    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    get_response = client.get(f"/users/{created_body["id"]}", headers=headers)
    get_body = get_response.json()

    assert created_response.status_code == 201
    assert get_response.status_code == 403

    assert len(get_body) == 1

    assert "detail" in get_body

    assert isinstance(get_body["detail"], str)

    assert get_body["detail"] == "Admin access required"