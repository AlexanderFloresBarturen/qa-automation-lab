from tests.helpers import assert_valid_user_response, assert_user_not_found_response

#region POSITIVOS
def test_get_user_success(client, created_user):
    response = client.get(f"/users/{created_user['id']}")
    body = response.json()

    assert response.status_code == 200

    assert_valid_user_response(body)

    assert body["id"] == created_user["id"]
    assert body["name"] == created_user["name"]
    assert body["email"] == created_user["email"]
    assert body["age"] == created_user["age"]

#endregion

#region NEGATIVOS
def test_get_user_not_found(client):
    response = client.get("/users/9999")
    body = response.json()

    assert response.status_code == 404

    assert_user_not_found_response(body)

#endregion