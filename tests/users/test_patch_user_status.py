from tests.helpers import assert_user_not_found_response, assert_valid_user_response_admin


def test_patch_user_status_success(client, admin_user, user_payload):
    user_one = user_payload()
    register_response = client.post("/auth/register", json=user_one)
    register_body = register_response.json()

    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"

    delete_response = client.delete(f"/users/{register_body["id"]}", headers=headers)

    status_payload = {}
    status_payload["is_active"] = True
    patch_status_response = client.patch(f"/users/{register_body["id"]}/status", json=status_payload, headers=headers)
    patch_status_body = patch_status_response.json()

    assert register_response.status_code == 201
    assert delete_response.status_code == 204
    assert patch_status_response.status_code == 200

    assert_valid_user_response_admin(patch_status_body)

    assert register_body["id"] == patch_status_body["id"]
    assert register_body["name"] == patch_status_body["name"]
    assert register_body["email"] == patch_status_body["email"]
    assert register_body["age"] == patch_status_body["age"]
    assert patch_status_body["is_active"] is True


def test_patch_user_status_already_active(client, admin_user, user_payload):
    user_one = user_payload()
    register_response = client.post("/auth/register", json=user_one)
    register_body = register_response.json()

    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"

    status_payload = {}
    status_payload["is_active"] = True
    patch_status_response = client.patch(f"/users/{register_body["id"]}/status", json=status_payload, headers=headers)
    patch_status_body = patch_status_response.json()

    assert register_response.status_code == 201
    assert patch_status_response.status_code == 404

    assert_user_not_found_response(patch_status_body)


def test_patch_user_status_not_found(client, admin_user):
    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"

    status_payload = {}
    status_payload["is_active"] = True
    patch_status_response = client.patch("/users/99999/status", json=status_payload, headers=headers)
    patch_status_body = patch_status_response.json()

    assert patch_status_response.status_code == 404

    assert_user_not_found_response(patch_status_body)


def test_patch_user_status_already_deactivated(client, admin_user, user_payload):
    user_one = user_payload()
    register_response = client.post("/auth/register", json=user_one)
    register_body = register_response.json()

    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"

    delete_response = client.delete(f"/users/{register_body["id"]}", headers=headers)

    status_payload = {}
    status_payload["is_active"] = False
    patch_status_response = client.patch(f"/users/{register_body["id"]}/status", json=status_payload, headers=headers)
    patch_status_body = patch_status_response.json()

    assert register_response.status_code == 201
    assert delete_response.status_code == 204
    assert patch_status_response.status_code == 409

    assert len(patch_status_body) == 1

    assert "detail" in patch_status_body

    assert isinstance(patch_status_body["detail"], str)

    assert patch_status_body["detail"] == "User already deactivated"
