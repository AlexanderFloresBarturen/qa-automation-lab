from typing import Any

from tests.helpers import assert_duplicate_email_response, assert_user_not_found_response, assert_valid_user_response_admin

# region POSITIVOS

def test_update_user_success(client, admin_user, user_payload, valid_update_payload):
    user_payload = user_payload()
    register_response = client.post("auth/register", json=user_payload)
    register_body = register_response.json()
    
    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"
    update_response = client.put(f"users/{register_body["id"]}", headers=headers, json=valid_update_payload)
    body_update = update_response.json()

    get_response = client.get(f"users/{register_body["id"]}", headers=headers)
    body_get = get_response.json()

    assert update_response.status_code == 200
    assert get_response.status_code == 200

    assert_valid_user_response_admin(body_get)

    assert body_update["name"] == valid_update_payload["name"]
    assert body_update["email"] == valid_update_payload["email"]
    assert body_update["age"] == valid_update_payload["age"]

    # Se verifica que los cambios se han reflejado en la DB
    assert body_get["name"] == valid_update_payload["name"]
    assert body_get["email"] == valid_update_payload["email"]
    assert body_get["age"] == valid_update_payload["age"]


# endregion


# region NEGATIVOS
def test_update_user_not_found(client, admin_user, valid_update_payload):
    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"
    response = client.put("/users/99999", headers=headers, json=valid_update_payload)
    body = response.json()

    assert response.status_code == 404

    assert_user_not_found_response(body)


def test_update_user_duplicate_email(client, user_payload, admin_user, valid_update_payload):
    user_one = user_payload()
    user_two = user_payload()

    register_response_one = client.post("/auth/register", json=user_one)
    register_body_one = register_response_one.json()

    register_response_two = client.post("/auth/register", json=user_two)
    register_body_two = register_response_two.json()

    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"
    update_payload = valid_update_payload.copy()
    update_payload["email"] = register_body_two["email"]
    put_response = client.put(f"/users/{register_body_one["id"]}", headers=headers, json=update_payload)
    body_put = put_response.json()

    assert register_response_one.status_code == 201
    assert register_response_two.status_code == 201
    assert put_response.status_code == 409

    assert_duplicate_email_response(body_put)

def test_update_user_standard_user(client, user_payload, loged_user, valid_update_payload):
    user_one = user_payload()

    register_response = client.post("/auth/register", json=user_one)
    register_body = register_response.json()

    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    update_payload = valid_update_payload.copy()
    update_response = client.put(f"/users/{register_body["id"]}", headers=headers, json=update_payload)
    update_body = update_response.json()

    assert register_response.status_code == 201
    assert update_response.status_code == 403

    assert "detail" in update_body

    assert update_body["detail"] == "Admin access required"

def test_update_user_empty_payload(client, user_payload, admin_user):
    user_one = user_payload()

    register_response = client.post("/auth/register", json=user_one)
    
    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"
    payload: dict[str, Any] = {}
    response = client.post("/users", json=payload, headers=headers)
    body = response.json()

    assert response.status_code == 422
    assert "detail" in body
    assert "type" in body["detail"][0]
    assert "type" in body["detail"][1]
    assert "type" in body["detail"][2]
    assert body["detail"][0]["type"] == "missing"
    assert body["detail"][1]["type"] == "missing"
    assert body["detail"][2]["type"] == "missing"
    assert "loc" in body["detail"][0]
    assert "loc" in body["detail"][1]
    assert "loc" in body["detail"][2]
    assert body["detail"][0]["loc"] == ["body", "name"]
    assert body["detail"][1]["loc"] == ["body", "email"]
    assert body["detail"][2]["loc"] == ["body", "age"]

# endregion