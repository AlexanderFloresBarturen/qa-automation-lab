from typing import Any

import pytest

from tests.helpers import assert_duplicate_email_response, assert_invalid_token_response, assert_not_authenticated_response, assert_not_found_response, assert_valid_user_response


# region POSITIVOS
def test_patch_user_name_success(loged_user, patch_user):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    patch_response = patch_user(name=True, headers=headers)
    body_patch = patch_response.json()

    assert patch_response.status_code == 200

    assert_valid_user_response(body_patch)

    assert loged_user["id"] == body_patch["id"]
    assert loged_user["name"] != body_patch["name"]
    assert loged_user["email"] == body_patch["email"]
    assert loged_user["age"] == body_patch["age"]


def test_patch_user_email_success(loged_user, patch_user):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    patch_response = patch_user(email=True, headers=headers)
    body_patch = patch_response.json()

    assert patch_response.status_code == 200

    assert_valid_user_response(body_patch)

    assert loged_user["id"] == body_patch["id"]
    assert loged_user["name"] == body_patch["name"]
    assert loged_user["email"] != body_patch["email"]
    assert loged_user["age"] == body_patch["age"]


def test_patch_user_age_success(loged_user, patch_user):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    patch_response = patch_user(age=True, headers=headers)
    body_patch = patch_response.json()

    assert patch_response.status_code == 200

    assert_valid_user_response(body_patch)

    assert loged_user["id"] == body_patch["id"]
    assert loged_user["name"] == body_patch["name"]
    assert loged_user["email"] == body_patch["email"]
    assert loged_user["age"] != body_patch["age"]


def test_patch_user_name_email_success(loged_user, patch_user):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    patch_response = patch_user(name=True, email=True, headers=headers)
    body_patch = patch_response.json()

    assert patch_response.status_code == 200

    assert_valid_user_response(body_patch)

    assert loged_user["id"] == body_patch["id"]
    assert loged_user["name"] != body_patch["name"]
    assert loged_user["email"] != body_patch["email"]
    assert loged_user["age"] == body_patch["age"]


def test_patch_user_name_age_success(loged_user, patch_user):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    patch_response = patch_user(name=True, age=True, headers=headers)
    body_patch = patch_response.json()

    assert patch_response.status_code == 200

    assert_valid_user_response(body_patch)

    assert loged_user["id"] == body_patch["id"]
    assert loged_user["name"] != body_patch["name"]
    assert loged_user["email"] == body_patch["email"]
    assert loged_user["age"] != body_patch["age"]


def test_patch_user_email_age_success(loged_user, patch_user):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    patch_response = patch_user(email=True, age=True, headers=headers)
    body_patch = patch_response.json()

    assert patch_response.status_code == 200

    assert_valid_user_response(body_patch)

    assert loged_user["id"] == body_patch["id"]
    assert loged_user["name"] == body_patch["name"]
    assert loged_user["email"] != body_patch["email"]
    assert loged_user["age"] != body_patch["age"]


def test_patch_user_full_success(loged_user, patch_user):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    patch_response = patch_user(name=True, email=True, age=True, headers=headers)
    body_patch = patch_response.json()

    assert patch_response.status_code == 200

    assert_valid_user_response(body_patch)

    assert loged_user["id"] == body_patch["id"]
    assert loged_user["name"] != body_patch["name"]
    assert loged_user["email"] != body_patch["email"]
    assert loged_user["age"] != body_patch["age"]


def test_patch_reuse_email(client, user_payload, get_token):
    user_one = user_payload()
    user_two = user_payload()

    post_response_first = client.post("/auth/register", json=user_one)
    body_post_first = post_response_first.json()

    post_response_second = client.post("/auth/register", json=user_two)
    body_post_second = post_response_second.json()

    token_user_one = get_token(username=user_one["email"], password=user_one["password"])
    headers_user_one = {}
    headers_user_one["Authorization"] = f"Bearer {token_user_one}"
    delete_response = client.delete("/profile", headers=headers_user_one)

    token_user_two = get_token(username=user_two["email"], password=user_two["password"])
    headers_user_two = {}
    headers_user_two["Authorization"] = f"Bearer {token_user_two}"
    patch_payload = {}
    patch_payload["email"] = f"{body_post_first['email']}"
    patch_response = client.patch("/profile", headers=headers_user_two, json=patch_payload)
    body_patch = patch_response.json()

    assert delete_response.status_code == 204
    assert patch_response.status_code == 200

    assert_valid_user_response(body_patch)

    assert body_post_second["id"] == body_patch["id"]
    assert body_post_second["name"] == body_patch["name"]
    assert body_post_second["email"] != body_patch["email"]
    assert body_post_second["age"] == body_patch["age"]

    assert body_patch["email"] == body_post_first["email"]


# endregion


# region NEGATIVOS
def test_patch_user_not_found(client, loged_user):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    patch_payload: dict[str, Any] = {}
    patch_payload["name"] = "someone"
    patch_response = client.patch("/profile/99999", json=patch_payload, headers=headers)
    body_patch = patch_response.json()

    assert patch_response.status_code == 404

    assert_not_found_response(body_patch)


def test_patch_deleted_user(client, loged_user, patch_user):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    delete_response = client.delete("/profile", headers=headers)

    patch_response = patch_user(name=True, headers=headers)
    body_patch = patch_response.json()

    assert delete_response.status_code == 204
    assert patch_response.status_code == 401

    assert_invalid_token_response(body_patch)


def test_patch_user_duplicate_email(client, user_payload, loged_user):
    user_two = user_payload()

    post_response_two = client.post("/auth/register", json=user_two)
    body_post_second = post_response_two.json()

    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    patch_payload = {}
    patch_payload["email"] = f"{body_post_second['email']}"
    patch_response = client.patch("/profile", headers=headers, json=patch_payload)
    body_patch = patch_response.json()

    assert patch_response.status_code == 409

    assert_duplicate_email_response(body_patch)


def test_patch_empty_payload(client, loged_user):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    patch_response = client.patch("/profile", headers=headers, json={})
    body_patch = patch_response.json()

    assert patch_response.status_code == 422

    assert "detail" in body_patch
    assert "type" in body_patch["detail"][0]
    assert "msg" in body_patch["detail"][0]

    assert body_patch["detail"][0]["type"] == "value_error"
    assert body_patch["detail"][0]["msg"] == "Value error, At least one field is required"


def test_patch_user_without_token(loged_user, patch_user):
    patch_response = patch_user(name=True)
    patch_body = patch_response.json()

    assert patch_response.status_code == 401

    assert_not_authenticated_response(patch_body)


def test_patch_user_invalid_token(loged_user, patch_user):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    patch_response = patch_user(name=True, headers={"Authorization": "Bearer invalid_token"})
    patch_body = patch_response.json()

    assert patch_response.status_code == 401

    assert_invalid_token_response(patch_body)


def test_patch_another_user(client, user_payload, loged_user, patch_user):
    user_two = user_payload()

    created_response_two = client.post("/auth/register", json=user_two)
    created_body_two = created_response_two.json()

    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    patch_payload: dict[str, Any] = {}
    patch_payload["name"] = "someone"
    patch_response = client.patch(f"/profile/{created_body_two["id"]}", json=patch_payload, headers=headers)
    patch_body = patch_response.json()

    assert created_response_two.status_code == 201
    assert patch_response.status_code == 404

    assert_not_found_response(patch_body)


# endregion

# region Parametrización
"""
Parametrización sirve para ejecutar un mismo test varias veces
con distintos conjuntos de datos, en este caso:
- test_patch_invalid_name
- test_patch_invalid_email
- test_patch_invalid_age
"""


@pytest.mark.parametrize(
    "payload, error_type, error_loc",
    [({"name": "A"}, "string_too_short", ["body", "name"]), ({"email": "correo"}, "value_error", ["body", "email"]), ({"age": 5}, "greater_than_equal", ["body", "age"])],
)
def test_patch_invalid_fields(client, loged_user, payload, error_type, error_loc):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    patch_response = client.patch("/profile", headers=headers, json=payload)
    body_patch = patch_response.json()

    assert patch_response.status_code == 422

    assert "detail" in body_patch
    assert "type" in body_patch["detail"][0]
    assert "loc" in body_patch["detail"][0]

    assert body_patch["detail"][0]["type"] == error_type
    assert body_patch["detail"][0]["loc"] == error_loc


@pytest.mark.parametrize(
    "payload, msg", [({"name": None}, "Value error, Field name cannot be null"), ({"email": None}, "Value error, Field email cannot be null"), ({"age": None}, "Value error, Field age cannot be null")]
)
def test_patch_null_fields(client, loged_user, payload, msg):
    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    patch_response = client.patch("/profile", headers=headers, json=payload)
    body_patch = patch_response.json()

    assert patch_response.status_code == 422

    assert "detail" in body_patch
    assert "type" in body_patch["detail"][0]
    assert "msg" in body_patch["detail"][0]

    assert body_patch["detail"][0]["type"] == "value_error"
    assert body_patch["detail"][0]["msg"] == msg


# endregion
