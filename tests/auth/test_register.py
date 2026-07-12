from typing import Any

import pytest

from tests.helpers import assert_valid_user_response


# region POSITIVOS
def test_register_user_success(client, valid_user_payload):
    response = client.post("/auth/register", json=valid_user_payload)
    body = response.json()

    assert response.status_code == 201

    assert_valid_user_response(body)

    assert body["name"] == valid_user_payload["name"]
    assert body["email"] == valid_user_payload["email"]
    assert body["age"] == valid_user_payload["age"]


# endregion


# region NEGATIVOS
def test_register_user_duplicate_email(client, user_payload):
    user_first = user_payload()
    user_second = user_payload()

    response_first = client.post("/auth/register", json=user_first)

    user_second["email"] = user_first["email"]
    response_second = client.post("/auth/register", json=user_second)
    body_second = response_second.json()

    assert response_first.status_code == 201
    assert response_second.status_code == 409

    assert "detail" in body_second

    assert body_second["detail"] == "Email already exists"


def test_register_user_name_too_short(client, valid_user_payload):
    payload = valid_user_payload.copy()
    payload["name"] = "A"

    response = client.post("/auth/register", json=payload)
    body = response.json()

    assert response.status_code == 422
    assert "detail" in body
    assert "type" in body["detail"][0]
    assert body["detail"][0]["type"] == "string_too_short"
    assert "loc" in body["detail"][0]
    assert body["detail"][0]["loc"] == ["body", "name"]


def test_register_user_missing_age(client):
    payload = {"name": "Alex", "email": "alex@gmail.com"}

    response = client.post("/auth/register", json=payload)
    body = response.json()

    assert response.status_code == 422
    assert "detail" in body
    assert "type" in body["detail"][0]
    assert body["detail"][0]["type"] == "missing"
    assert "loc" in body["detail"][0]
    assert body["detail"][0]["loc"] == ["body", "age"]


def test_register_user_empty_payload(client):
    payload: dict[str, Any] = {}

    response = client.post("/auth/register", json=payload)
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


@pytest.mark.parametrize(
    "password, type, error_message",
    [
        ("password123!", "value_error", "The password must contain at least one uppercase letter"),
        ("PASSWORD123!", "value_error", "The password must contain at least one lowercase letter"),
        ("Password!!!", "value_error", "The password must contain at least one number"),
        ("Password123", "value_error", "The password must contain at least one special character"),
        ("Pass1!", "string_too_short", "String should have at least 8 characters"),
    ],
)
def test_register_user_invalid_password(client, user_payload, password, type, error_message):
    payload = user_payload(password=password)
    response = client.post("/auth/register", json=payload)
    body = response.json()

    assert response.status_code == 422

    assert "detail" in body
    assert "loc" in body["detail"][0]
    assert "type" in body["detail"][0]
    assert "msg" in body["detail"][0]

    assert body["detail"][0]["loc"] == ["body", "password"]
    assert body["detail"][0]["type"] == type
    assert error_message in body["detail"][0]["msg"]


# endregion
