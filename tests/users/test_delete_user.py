from tests.helpers import assert_user_not_found_response

# region POSITIVOS

def test_delete_user_success(client, user_payload, admin_user):
    user_one = user_payload()
    register_response = client.post("/auth/register", json=user_one)
    register_body = register_response.json()

    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"
    delete_response = client.delete(f"/users/{register_body["id"]}", headers=headers)

    get_response = client.get(f"/users/{register_body["id"]}", headers=headers)
    get_body = get_response.json()

    assert register_response.status_code == 201
    assert delete_response.status_code == 204
    assert get_response.status_code == 200

    get_body["is_active"] is False
    get_body["id"] == register_body["id"]
    get_body["name"] == register_body["name"]
    get_body["age"] == register_body["age"]


# endregion

# region NEGATIVOS
def test_delete_user_not_found(client, admin_user):
    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"
    delete_response = client.delete("/users/99999", headers=headers)
    delete_body = delete_response.json()

    assert delete_response.status_code == 404

    assert_user_not_found_response(delete_body)


def test_delete_user_twice(client, user_payload, admin_user):
    user_one = user_payload()

    register_response = client.post("/auth/register", json=user_one)
    register_body = register_response.json()

    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"
    delete_response_first = client.delete(f"/users/{register_body["id"]}", headers=headers)

    delete_response_second = client.delete(f"/users/{register_body["id"]}", headers=headers)
    body_delete_second = delete_response_second.json()

    assert register_response.status_code == 201
    assert delete_response_first.status_code == 204
    assert delete_response_second.status_code == 404

    assert_user_not_found_response(body_delete_second)

def test_delete_user_itself(client, admin_user):
    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"
    delete_response = client.delete(f"/users/{admin_user["id"]}", headers=headers)
    delete_body = delete_response.json()

    assert delete_response.status_code == 400

    assert len(delete_body) == 1

    assert "detail" in delete_body
    
    assert isinstance(delete_body["detail"], str)

    assert delete_body["detail"] == "Use DELETE /profile to delete your own account."

# endregion