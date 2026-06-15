import pytest

#region POSITIVOS
def test_patch_user_name_success(created_user, patch_user):
    patch_response = patch_user(id=created_user["id"], name=True)
    body_patch = patch_response.json()

    assert patch_response.status_code == 200

    assert len(body_patch) == 4

    assert "id" in body_patch
    assert "name" in body_patch
    assert "email" in body_patch
    assert "age" in body_patch

    assert isinstance(body_patch["id"], int)
    assert isinstance(body_patch["age"], int)
    assert isinstance(body_patch["name"], str)
    assert isinstance(body_patch["email"], str)

    assert created_user["id"] == body_patch["id"]
    assert created_user["name"] != body_patch["name"]
    assert created_user["email"] == body_patch["email"]
    assert created_user["age"] == body_patch["age"]

def test_patch_user_email_success(created_user, patch_user):
    patch_response = patch_user(id=created_user["id"], email=True)
    body_patch = patch_response.json()

    assert patch_response.status_code == 200

    assert len(body_patch) == 4

    assert "id" in body_patch
    assert "name" in body_patch
    assert "email" in body_patch
    assert "age" in body_patch

    assert isinstance(body_patch["id"], int)
    assert isinstance(body_patch["age"], int)
    assert isinstance(body_patch["name"], str)
    assert isinstance(body_patch["email"], str)

    assert created_user["id"] == body_patch["id"]
    assert created_user["name"] == body_patch["name"]
    assert created_user["email"] != body_patch["email"]
    assert created_user["age"] == body_patch["age"]

def test_patch_user_age_success(created_user, patch_user):
    patch_response = patch_user(id=created_user["id"], age=True)
    body_patch = patch_response.json()

    assert patch_response.status_code == 200

    assert len(body_patch) == 4

    assert "id" in body_patch
    assert "name" in body_patch
    assert "email" in body_patch
    assert "age" in body_patch

    assert isinstance(body_patch["id"], int)
    assert isinstance(body_patch["age"], int)
    assert isinstance(body_patch["name"], str)
    assert isinstance(body_patch["email"], str)

    assert created_user["id"] == body_patch["id"]
    assert created_user["name"] == body_patch["name"]
    assert created_user["email"] == body_patch["email"]
    assert created_user["age"] != body_patch["age"]

def test_patch_user_name_email_success(created_user, patch_user):
    patch_response = patch_user(id=created_user["id"], name=True, email=True)
    body_patch = patch_response.json()

    assert patch_response.status_code == 200

    assert len(body_patch) == 4

    assert "id" in body_patch
    assert "name" in body_patch
    assert "email" in body_patch
    assert "age" in body_patch

    assert isinstance(body_patch["id"], int)
    assert isinstance(body_patch["age"], int)
    assert isinstance(body_patch["name"], str)
    assert isinstance(body_patch["email"], str)

    assert created_user["id"] == body_patch["id"]
    assert created_user["name"] != body_patch["name"]
    assert created_user["email"] != body_patch["email"]
    assert created_user["age"] == body_patch["age"]

def test_patch_user_name_age_success(created_user, patch_user):
    patch_response = patch_user(id=created_user["id"], name=True, age=True)
    body_patch = patch_response.json()

    assert patch_response.status_code == 200

    assert len(body_patch) == 4

    assert "id" in body_patch
    assert "name" in body_patch
    assert "email" in body_patch
    assert "age" in body_patch

    assert isinstance(body_patch["id"], int)
    assert isinstance(body_patch["age"], int)
    assert isinstance(body_patch["name"], str)
    assert isinstance(body_patch["email"], str)

    assert created_user["id"] == body_patch["id"]
    assert created_user["name"] != body_patch["name"]
    assert created_user["email"] == body_patch["email"]
    assert created_user["age"] != body_patch["age"]

def test_patch_user_email_age_success(created_user, patch_user):
    patch_response = patch_user(id=created_user["id"], email=True, age=True)
    body_patch = patch_response.json()

    assert patch_response.status_code == 200

    assert len(body_patch) == 4

    assert "id" in body_patch
    assert "name" in body_patch
    assert "email" in body_patch
    assert "age" in body_patch

    assert isinstance(body_patch["id"], int)
    assert isinstance(body_patch["age"], int)
    assert isinstance(body_patch["name"], str)
    assert isinstance(body_patch["email"], str)

    assert created_user["id"] == body_patch["id"]
    assert created_user["name"] == body_patch["name"]
    assert created_user["email"] != body_patch["email"]
    assert created_user["age"] != body_patch["age"]

def test_patch_user_full_success(created_user, patch_user):
    patch_response = patch_user(id=created_user["id"], name=True, email=True, age=True)
    body_patch = patch_response.json()

    assert patch_response.status_code == 200

    assert len(body_patch) == 4

    assert "id" in body_patch
    assert "name" in body_patch
    assert "email" in body_patch
    assert "age" in body_patch

    assert isinstance(body_patch["id"], int)
    assert isinstance(body_patch["age"], int)
    assert isinstance(body_patch["name"], str)
    assert isinstance(body_patch["email"], str)

    assert created_user["id"] == body_patch["id"]
    assert created_user["name"] != body_patch["name"]
    assert created_user["email"] != body_patch["email"]
    assert created_user["age"] != body_patch["age"]

def test_patch_reuse_email(client, user_payload):
    user_first = user_payload()
    user_second = user_payload()

    post_response_first = client.post("/users", json=user_first)
    body_post_first = post_response_first.json()
    
    post_response_second = client.post("/users", json=user_second)
    body_post_second = post_response_second.json()

    delete_response = client.delete(f"/users/{body_post_first['id']}")

    patch_payload = {}
    patch_payload["email"] = f"{body_post_first['email']}"
    patch_response = client.patch(f"/users/{body_post_second['id']}", json=patch_payload)
    body_patch = patch_response.json()

    assert delete_response.status_code == 204
    assert patch_response.status_code == 200

    assert len(body_patch) == 4

    assert "id" in body_patch
    assert "name" in body_patch
    assert "email" in body_patch
    assert "age" in body_patch

    assert isinstance(body_patch["id"], int)
    assert isinstance(body_patch["age"], int)
    assert isinstance(body_patch["name"], str)
    assert isinstance(body_patch["email"], str)

    assert body_post_second["id"] == body_patch["id"]
    assert body_post_second["name"] == body_patch["name"]
    assert body_post_second["email"] != body_patch["email"]
    assert body_post_second["age"] == body_patch["age"]

    assert body_patch["email"] == body_post_first["email"]

#endregion

#region NEGATIVOS
def test_patch_user_not_found(patch_user):
    patch_response = patch_user(id=9999, name = True)
    body_patch = patch_response.json()

    assert patch_response.status_code == 404

    assert len(body_patch) == 1

    assert "detail" in body_patch

    assert body_patch["detail"] == "User not found"

def test_patch_deleted_user(client, created_user, patch_user):
    delete_response = client.delete(f"/users/{created_user['id']}")

    patch_response = patch_user(id=created_user["id"], name=True)
    body_patch = patch_response.json()

    assert delete_response.status_code == 204
    assert patch_response.status_code == 404

    assert len(body_patch) == 1

    assert "detail" in body_patch

    assert body_patch["detail"] == "User not found"

def test_patch_user_duplicate_email(client, user_payload):
    user_first = user_payload()
    user_second = user_payload()

    post_response_first = client.post("/users", json=user_first)
    
    post_response_second = client.post("/users", json=user_second)
    body_post_second = post_response_second.json()

    patch_payload = {}
    patch_payload["email"] = f"{user_first['email']}"
    patch_response = client.patch(f"/users/{body_post_second['id']}", json=patch_payload)
    body_patch = patch_response.json()

    assert patch_response.status_code == 409

    assert len(body_patch) == 1

    assert "detail" in body_patch

    assert body_patch["detail"] == "Email already exists"

def test_patch_empty_payload(client, created_user):
    patch_response = client.patch(f"/users/{created_user['id']}", json={})
    body_patch = patch_response.json()

    assert patch_response.status_code == 422

    assert "detail" in body_patch
    assert "type" in body_patch["detail"][0]
    assert "msg" in body_patch["detail"][0]

    assert body_patch["detail"][0]["type"] == "value_error"
    assert body_patch["detail"][0]["msg"] == "Value error, At least one field is required"

#endregion

#region Parametrización
"""
Parametrización sirve para ejecutar un mismo test varias veces
con distintos conjuntos de datos, en este caso:
- test_patch_invalid_name
- test_patch_invalid_email
- test_patch_invalid_age
"""
@pytest.mark.parametrize(
    "payload, error_type, error_loc",
    [
        ({"name": "A"}, "string_too_short", ["body", "name"]),
        ({"email": "correo"}, "value_error", ["body", "email"]),
        ({"age": 5}, "greater_than_equal", ["body", "age"])
    ]
)
def test_patch_invalid_fields(client, created_user, payload, error_type, error_loc):
    patch_response = client.patch(f"/users/{created_user['id']}", json=payload)
    body_patch = patch_response.json()

    assert patch_response. status_code == 422

    assert "detail" in body_patch
    assert "type" in body_patch["detail"][0]
    assert "loc" in body_patch["detail"][0]

    assert body_patch["detail"][0]["type"] == error_type
    assert body_patch["detail"][0]["loc"] == error_loc

@pytest.mark.parametrize(
    "payload, msg",
    [
        ({"name": None}, "Value error, Field name cannot be null"),
        ({"email": None}, "Value error, Field email cannot be null"),
        ({"age": None}, "Value error, Field age cannot be null")
    ]
)
def test_patch_null_fields(client, created_user, payload, msg):
    patch_response = client.patch(f"/users/{created_user['id']}", json=payload)
    body_patch = patch_response.json()

    assert patch_response.status_code == 422

    assert "detail" in body_patch
    assert "type" in body_patch["detail"][0]
    assert "msg" in body_patch["detail"][0]

    assert body_patch["detail"][0]["type"] == "value_error"
    assert body_patch["detail"][0]["msg"] == msg

#endregion