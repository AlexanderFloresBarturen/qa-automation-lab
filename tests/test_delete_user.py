def test_delete_user_success(client, created_user):
    delete_response = client.delete(f"/users/{created_user['id']}")
    
    get_response = client.get(f"/users/{created_user['id']}")
    body_get = get_response.json()

    assert delete_response.status_code == 204
    assert get_response.status_code == 404

    assert "detail" in body_get

    assert body_get["detail"] == "User not found"

def test_delete_user_not_found(client):
    response = client.delete("/users/0")
    body = response.json()

    assert response.status_code == 404

    assert "detail" in body

    assert body["detail"] == "User not found"

def test_delete_user_twice(client, created_user):
    delete_response_first = client.delete(f"/users/{created_user['id']}")

    delete_response_second = client.delete(f"/users/{created_user['id']}")
    body_delete_second = delete_response_second.json()

    assert delete_response_first.status_code == 204
    assert delete_response_second.status_code == 404

    assert "detail" in body_delete_second

    assert body_delete_second["detail"] == "User not found"