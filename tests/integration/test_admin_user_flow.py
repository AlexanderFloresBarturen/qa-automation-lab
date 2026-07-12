def test_admin_user_management_end_to_end(client, admin_user, user_payload, valid_update_payload, patch_user):
    user = user_payload(name="Bob")

    headers = {}
    headers["Authorization"] = f"Bearer {admin_user["token"]}"

    create_response = client.post("users/", json=user, headers=headers)
    create_body = create_response.json()

    assert create_response.status_code == 201

    get_response_one = client.get(f"/users/{create_body["id"]}", headers=headers)
    get_body_one = get_response_one.json()

    assert get_response_one.status_code == 200

    assert get_body_one["is_active"] is True
    assert get_body_one["id"] == create_body["id"]
    assert get_body_one["name"] == create_body["name"]
    assert get_body_one["email"] == create_body["email"]
    assert get_body_one["age"] == create_body["age"]

    update_response = client.put(f"/users/{create_body["id"]}", json=valid_update_payload, headers=headers)
    update_body = update_response.json()

    assert update_response.status_code == 200

    assert update_body["is_active"] is True
    assert update_body["id"] == get_body_one["id"]
    assert update_body["name"] != get_body_one["name"]
    assert update_body["email"] != get_body_one["email"]
    assert update_body["age"] != get_body_one["age"]

    patch_response = patch_user(name=True, is_admin=True, user_id=create_body["id"], headers=headers)
    patch_body = patch_response.json()

    assert patch_body["is_active"] is True
    assert patch_body["id"] == update_body["id"]
    assert patch_body["name"] != update_body["id"]
    assert patch_body["email"] == update_body["email"]
    assert patch_body["age"] == update_body["age"]

    delete_response = client.delete(f"/users/{create_body["id"]}", headers=headers)

    assert delete_response.status_code == 204

    get_response_two = client.get("/users/", headers=headers)
    get_body_two = get_response_two.json()

    assert get_response_two.status_code == 200

    assert isinstance(get_body_two, list)

    assert len(get_body_two) == 2

    assert get_body_two[1]["id"] == create_body["id"]
    assert get_body_two[1]["is_active"] is False
