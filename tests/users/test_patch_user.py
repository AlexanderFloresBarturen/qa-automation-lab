# region POSITIVOS
from typing import Any

from tests.helpers import assert_duplicate_email_response, assert_user_not_found_response, assert_valid_user_response


def test_patch_user_name_success(client, admin_user, user_payload, patch_user):
    user_one = user_payload()
    register_response = client.post("/auth/register", json=user_one)
    register_body = register_response.json()

    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"
    patch_response = patch_user(name=True, is_admin=True, user_id=register_body["id"], headers=headers)
    body_patch = patch_response.json()

    assert register_response.status_code == 201
    assert patch_response.status_code == 200

    assert_valid_user_response(body_patch)

    assert register_body["id"] == body_patch["id"]
    assert register_body["name"] != body_patch["name"]
    assert register_body["email"] == body_patch["email"]
    assert register_body["age"] == body_patch["age"]


def test_patch_user_email_success(client, admin_user, user_payload, patch_user):
    user_one = user_payload()
    register_response = client.post("/auth/register", json=user_one)
    register_body = register_response.json()

    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"
    patch_response = patch_user(email=True, is_admin=True, user_id=register_body["id"], headers=headers)
    body_patch = patch_response.json()

    assert register_response.status_code == 201
    assert patch_response.status_code == 200

    assert_valid_user_response(body_patch)

    assert register_body["id"] == body_patch["id"]
    assert register_body["name"] == body_patch["name"]
    assert register_body["email"] != body_patch["email"]
    assert register_body["age"] == body_patch["age"]


def test_patch_user_age_success(client, admin_user, user_payload, patch_user):
    user_one = user_payload()
    register_response = client.post("/auth/register", json=user_one)
    register_body = register_response.json()

    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"
    patch_response = patch_user(age=True, is_admin=True, user_id=register_body["id"], headers=headers)
    body_patch = patch_response.json()

    assert register_response.status_code == 201
    assert patch_response.status_code == 200

    assert_valid_user_response(body_patch)

    assert register_body["id"] == body_patch["id"]
    assert register_body["name"] == body_patch["name"]
    assert register_body["email"] == body_patch["email"]
    assert register_body["age"] != body_patch["age"]


def test_patch_user_name_email_success(client, admin_user, user_payload, patch_user):
    user_one = user_payload()
    register_response = client.post("/auth/register", json=user_one)
    register_body = register_response.json()

    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"
    patch_response = patch_user(name=True, email=True, is_admin=True, user_id=register_body["id"], headers=headers)
    body_patch = patch_response.json()

    assert register_response.status_code == 201
    assert patch_response.status_code == 200

    assert_valid_user_response(body_patch)

    assert register_body["id"] == body_patch["id"]
    assert register_body["name"] != body_patch["name"]
    assert register_body["email"] != body_patch["email"]
    assert register_body["age"] == body_patch["age"]


def test_patch_user_name_age_success(client, admin_user, user_payload, patch_user):
    user_one = user_payload()
    register_response = client.post("/auth/register", json=user_one)
    register_body = register_response.json()

    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"
    patch_response = patch_user(name=True, age=True, is_admin=True, user_id=register_body["id"], headers=headers)
    body_patch = patch_response.json()

    assert register_response.status_code == 201
    assert patch_response.status_code == 200

    assert_valid_user_response(body_patch)

    assert register_body["id"] == body_patch["id"]
    assert register_body["name"] != body_patch["name"]
    assert register_body["email"] == body_patch["email"]
    assert register_body["age"] != body_patch["age"]


def test_patch_user_email_age_success(client, admin_user, user_payload, patch_user):
    user_one = user_payload()
    register_response = client.post("/auth/register", json=user_one)
    register_body = register_response.json()

    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"
    patch_response = patch_user(email=True, age=True, is_admin=True, user_id=register_body["id"], headers=headers)
    body_patch = patch_response.json()

    assert register_response.status_code == 201
    assert patch_response.status_code == 200

    assert_valid_user_response(body_patch)

    assert register_body["id"] == body_patch["id"]
    assert register_body["name"] == body_patch["name"]
    assert register_body["email"] != body_patch["email"]
    assert register_body["age"] != body_patch["age"]


def test_patch_user_full_success(client, admin_user, user_payload, patch_user):
    user_one = user_payload()
    register_response = client.post("/auth/register", json=user_one)
    register_body = register_response.json()

    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"
    patch_response = patch_user(name=True, email=True, age=True, is_admin=True, user_id=register_body["id"], headers=headers)
    body_patch = patch_response.json()

    assert register_response.status_code == 201
    assert patch_response.status_code == 200

    assert_valid_user_response(body_patch)

    assert register_body["id"] == body_patch["id"]
    assert register_body["name"] != body_patch["name"]
    assert register_body["email"] != body_patch["email"]
    assert register_body["age"] != body_patch["age"]


def test_patch_reuse_email(client, user_payload, get_token, admin_user):
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

    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"
    patch_payload = {}
    patch_payload["email"] = f"{body_post_first['email']}"
    patch_response = client.patch(f"/users/{body_post_second["id"]}", headers=headers, json=patch_payload)
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
def test_patch_user_not_found(client, admin_user):
    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"
    patch_payload: dict[str, Any] = {}
    patch_payload["name"] = "someone"
    patch_response = client.patch("/users/99999", json=patch_payload, headers=headers)
    body_patch = patch_response.json()

    assert patch_response.status_code == 404

    assert_user_not_found_response(body_patch)

def test_patch_user_duplicate_email(client, user_payload, admin_user):
    user_one = user_payload()
    user_two = user_payload()

    post_response_one = client.post("/auth/register", json=user_one)
    body_post_one = post_response_one.json()

    post_response_two = client.post("/auth/register", json=user_two)
    body_post_second = post_response_two.json()

    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"
    patch_payload = {}
    patch_payload["email"] = f"{body_post_one['email']}"
    patch_response = client.patch(f"/users/{body_post_second["id"]}", headers=headers, json=patch_payload)
    body_patch = patch_response.json()

    assert patch_response.status_code == 409

    assert_duplicate_email_response(body_patch)

def test_update_user_standard_user(client, user_payload, loged_user, patch_user):
    user_one = user_payload()

    register_response = client.post("/auth/register", json=user_one)
    register_body = register_response.json()

    headers = {}
    headers["Authorization"] = f"Bearer {loged_user["token"]}"
    patch_response = patch_user(name=True, is_admin=True, user_id=register_body["id"], headers=headers)
    body_patch = patch_response.json()

    assert register_response.status_code == 201
    assert patch_response.status_code == 403

    assert "detail" in body_patch

    assert body_patch["detail"] == "Admin access required"

# endregion