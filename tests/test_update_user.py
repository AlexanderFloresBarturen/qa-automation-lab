from tests.helpers import assert_valid_user_response, assert_duplicate_email_response, assert_forbidden_response, assert_not_authenticated_response, assert_invalid_token_response

#region POSITIVOS
def test_update_user_success(client, loged_user, valid_update_payload):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    update_response = client.put(f"/users/{loged_user['id']}", headers=headers, json=valid_update_payload)
    body_update = update_response.json()

    get_response = client.get(f"/users/{loged_user['id']}", headers=headers)
    body_get = get_response.json()

    assert update_response.status_code == 200
    assert get_response.status_code == 200

    assert_valid_user_response(body_get)

    assert body_update["id"] == loged_user["id"]

    assert body_update["name"] == valid_update_payload["name"]
    assert body_update["email"] == valid_update_payload["email"]
    assert body_update["age"] == valid_update_payload["age"]

    # Se verifica que los cambios se han reflejado en la DB
    assert body_get["name"] == valid_update_payload["name"]
    assert body_get["email"] == valid_update_payload["email"]
    assert body_get["age"] == valid_update_payload["age"]

#endregion

#region NEGATIVOS
def test_update_user_not_found(client, loged_user, valid_update_payload):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    response = client.put("/users/9999", headers=headers, json=valid_update_payload)
    body = response.json()

    assert response.status_code == 403

    assert_forbidden_response(body)

def test_update_user_duplicate_email(client, user_payload, loged_user, valid_update_payload):
    user_two = user_payload()

    client.post("/users", json=user_two)

    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    update_payload = valid_update_payload.copy()
    update_payload["email"] = user_two["email"]
    put_response = client.put(f"/users/{loged_user['id']}", headers=headers, json=update_payload)
    body_put = put_response.json()

    assert put_response.status_code == 409

    assert_duplicate_email_response(body_put)

def test_update_deleted_user(client, loged_user, valid_update_payload):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    client.delete(f"/users/{loged_user['id']}", headers=headers)

    update_response = client.put(f"/users/{loged_user['id']}", headers=headers, json=valid_update_payload)
    body_update = update_response.json()

    assert update_response.status_code == 401

    assert_invalid_token_response(body_update)

def test_update_user_without_token(client, created_user, valid_update_payload):
    update_response = client.put(f"/users/{created_user['id']}", json= valid_update_payload)
    update_body = update_response.json()

    assert update_response.status_code == 401

    assert_not_authenticated_response(update_body)

def test_update_user_invalid_token(client, created_user, valid_update_payload):
    update_response = client.put(f"/users/{created_user['id']}", headers={"Authorization": "Bearer invalid_token"}, json=valid_update_payload)
    update_body = update_response.json()

    assert update_response.status_code == 401

    assert_invalid_token_response(update_body)

def test_update_another_user(client, user_payload, loged_user, valid_update_payload):
    user_two = user_payload()

    created_response_two = client.post("/users", json=user_two)
    created_body_two = created_response_two.json()

    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    update_response = client.put(f"/users/{created_body_two['id']}", headers=headers, json=valid_update_payload)
    update_body = update_response.json()

    assert created_response_two.status_code == 201
    assert update_response.status_code == 403

    assert_forbidden_response(update_body)
    
#endregion