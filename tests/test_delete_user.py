from tests.helpers import assert_not_found_response, assert_invalid_token_response, assert_not_authenticated_response


# region POSITIVOS
def test_delete_user_success(client, loged_user):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    delete_response = client.delete("/profile", headers=headers)

    get_response = client.get("/profile", headers=headers)
    get_body = get_response.json()

    assert delete_response.status_code == 204
    assert get_response.status_code == 401

    assert_invalid_token_response(get_body)


# endregion


# region NEGATIVOS
def test_delete_user_not_found(client, loged_user):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    delete_response = client.delete("/profile/99999", headers=headers)
    delete_body = delete_response.json()

    assert delete_response.status_code == 404

    assert_not_found_response(delete_body)


def test_delete_user_twice(client, loged_user):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    delete_response_first = client.delete("/profile", headers=headers)

    delete_response_second = client.delete("/profile", headers=headers)
    body_delete_second = delete_response_second.json()

    assert delete_response_first.status_code == 204
    assert delete_response_second.status_code == 401

    assert_invalid_token_response(body_delete_second)


def test_delete_user_without_token(client, created_user):
    delete_response = client.delete("/profile")
    delete_body = delete_response.json()

    assert delete_response.status_code == 401

    assert_not_authenticated_response(delete_body)


def test_delete_user_invalid_token(client, created_user):
    delete_response = client.delete("/profile", headers={"Authorization": "Bearer invalid_token"})
    delete_body = delete_response.json()

    assert delete_response.status_code == 401

    assert_invalid_token_response(delete_body)


def test_delete_another_user(client, user_payload, loged_user):
    user_two = user_payload()

    created_response_two = client.post("/auth/register", json=user_two)
    created_body_two = created_response_two.json()

    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    delete_response = client.delete(f"/profile/{created_body_two['id']}", headers=headers)
    delete_body = delete_response.json()

    assert created_response_two.status_code == 201
    assert delete_response.status_code == 404

    assert_not_found_response(delete_body)


# endregion
