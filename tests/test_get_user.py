from tests.helpers import assert_valid_user_response, assert_forbidden_response, assert_not_authenticated_response, assert_invalid_token_response

#region POSITIVOS
def test_get_user_success(client, loged_user):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    get_response = client.get(f"/users/{loged_user['id']}", headers=headers)
    get_body = get_response.json()

    assert get_response.status_code == 200

    assert_valid_user_response(get_body)

    assert get_body["id"] == loged_user["id"]
    assert get_body["name"] == loged_user["name"]
    assert get_body["email"] == loged_user["email"]
    assert get_body["age"] == loged_user["age"]

#endregion

#region NEGATIVOS
def test_get_user_without_token(client, created_user):
    get_response = client.get(f"/users/{created_user['id']}")
    get_body = get_response.json()

    assert get_response.status_code == 401

    assert_not_authenticated_response(get_body)

def test_get_user_invalid_token(client, created_user):
    get_response = client.get(f"/users/{created_user['id']}", headers={"Authorization": "Bearer invalid_token"})
    get_body = get_response.json()

    assert get_response.status_code == 401

    assert_invalid_token_response(get_body)

def test_get_another_user(client, user_payload, loged_user):
    user_two = user_payload()

    created_response_two = client.post("/users", json=user_two)
    created_body_two = created_response_two.json()

    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    get_response = client.get(f"/users/{created_body_two['id']}", headers=headers)
    get_body = get_response.json()

    assert created_response_two.status_code == 201
    assert get_response.status_code == 403

    assert_forbidden_response(get_body)

def test_get_nonexisting_user(client, loged_user):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    get_response = client.get(f"/users/{99999}", headers=headers)
    get_body = get_response.json()

    assert get_response.status_code == 403

    assert_forbidden_response(get_body)

#endregion