from typing import Any

from tests.helpers import assert_invalid_token_response, assert_valid_user_response_admin


# region POSITIVOS
def test_create_user_success(client, admin_user, user_payload):
    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"
    payload = user_payload()
    post_response = client.post("/users", json=payload, headers=headers)
    post_body = post_response.json()

    assert post_response.status_code == 201

    assert_valid_user_response_admin(post_body)

    assert post_body["name"] == payload["name"]
    assert post_body["email"] == payload["email"]
    assert post_body["age"] == payload["age"]


# endregion


# region NEGATIVOS
def test_create_user_duplicate_email(client, admin_user, user_payload):
    user_first = user_payload()
    user_second = user_payload()

    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"

    response_first = client.post("/users", json=user_first, headers=headers)

    user_second["email"] = user_first["email"]
    response_second = client.post("/users", json=user_second, headers=headers)
    body_second = response_second.json()

    assert response_first.status_code == 201
    assert response_second.status_code == 409

    assert "detail" in body_second

    assert body_second["detail"] == "Email already exists"


def test_create_user_standard_user(client, loged_user, user_payload):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    payload = user_payload()
    post_response = client.post("/users", json=payload, headers=headers)
    post_body = post_response.json()

    assert post_response.status_code == 403

    assert "detail" in post_body

    assert post_body["detail"] == "Admin access required"


def test_create_user_invalid_token(client, user_payload):
    headers = {}
    headers["Authorization"] = "Bearer invalid token"
    payload = user_payload()
    post_response = client.post("/users", json=payload, headers=headers)
    post_body = post_response.json()

    assert post_response.status_code == 401

    assert_invalid_token_response(post_body)


def test_create_user_empty_payload(client, admin_user):
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
