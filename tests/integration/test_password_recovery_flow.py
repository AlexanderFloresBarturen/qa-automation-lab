def test_password_recovery_end_to_end(client, valid_user_payload):
    create_response = client.post("/users", json=valid_user_payload)

    login_payload = {}
    login_payload["username"] = valid_user_payload["email"]
    login_payload["password"] = valid_user_payload["password"]
    login_response = client.post("/users/login", data=login_payload)

    fp_response = client.post("/users/forgot-password", json={"email": valid_user_payload["email"]})
    fp_body = fp_response.json()

    new_password = "NewPassword123!"
    rp_payload = {"token": fp_body["token"], "new_password": new_password}
    rp_response = client.post("/users/reset-password", json=rp_payload)

    login_payload_old_pwd = {}
    login_payload_old_pwd["username"] = valid_user_payload["email"]
    login_payload_old_pwd["password"] = valid_user_payload["password"]
    login_response_old_pwd = client.post("/users/login", data=login_payload_old_pwd)

    login_payload_new_pwd = {}
    login_payload_new_pwd["username"] = valid_user_payload["email"]
    login_payload_new_pwd["password"] = new_password
    login_response_new_pwd = client.post("/users/login", data=login_payload_new_pwd)

    assert create_response.status_code == 201
    assert login_response.status_code == 200
    assert fp_response.status_code == 200
    assert rp_response.status_code == 200
    assert login_response_old_pwd.status_code == 401
    assert login_response_new_pwd.status_code == 200
