from datetime import datetime, timedelta

from app.models.user_model import UserModel

#region POSITIVOS
def test_login_user_success(client, valid_user_payload):
    create_response = client.post("/users", json=valid_user_payload)

    payload = {}
    payload["username"] = valid_user_payload["email"]
    payload["password"] = valid_user_payload["password"]
    login_response = client.post("/users/login", data=payload)
    login_body = login_response.json()

    assert create_response.status_code == 201
    assert login_response.status_code == 200

    assert len(login_body) == 2

    assert "access_token" in login_body
    assert "token_type" in login_body

#endregion

#region NEGATIVOS
def test_login_nonexisting_user(client, valid_user_payload):
    create_response = client.post("/users", json=valid_user_payload)

    payload = {}
    payload["username"] = "nonexisting@email.com"
    payload["password"] =  valid_user_payload["password"]
    login_response = client.post("/users/login", data=payload)
    login_body = login_response.json()

    assert create_response.status_code == 201
    assert login_response.status_code == 401

    assert len(login_body) == 1

    assert "detail" in login_body
    
    assert login_body["detail"] == "Invalid credentials"

def test_login_incorrect_password(client, valid_user_payload):
    create_response = client.post("/users", json=valid_user_payload)

    payload = {}
    payload["username"] = valid_user_payload["email"]
    payload["password"] =  "MuSuperPassword123!"
    login_response = client.post("/users/login", data=payload)
    login_body = login_response.json()

    assert create_response.status_code == 201
    assert login_response.status_code == 401

    assert len(login_body) == 1

    assert "detail" in login_body
    
    assert login_body["detail"] == "Invalid credentials"

#endregion

#region Tests de bloqueo de cuenta
def test_login_increments_failed_attempts(db, client, valid_user_payload):
    create_response = client.post("/users", json=valid_user_payload)

    user_before = db.query(UserModel).filter(
        UserModel.email == valid_user_payload["email"],
        UserModel.is_active.is_(True)
    ).first()

    db.expunge(user_before)

    payload = {}
    payload["username"] = valid_user_payload["email"]
    payload["password"] = "MySuperPassword123!"
    login_response = client.post("/users/login", data=payload)
    login_body = login_response.json()

    user_after = db.query(UserModel).filter(
        UserModel.email == valid_user_payload["email"], 
        UserModel.is_active.is_(True)
    ).first()
    
    assert create_response.status_code == 201
    assert login_response.status_code == 401

    assert len(login_body) == 1

    assert "detail" in login_body

    assert isinstance(login_body["detail"], str)
    
    assert login_body["detail"] == "Invalid credentials"
    assert user_before.failed_login_attempts == 0
    assert user_before.locked_until is None
    assert user_after.failed_login_attempts == 1
    assert user_after.locked_until is None

def test_account_locked_after_five_attempts(db, client, valid_user_payload):
    create_response = client.post("/users", json=valid_user_payload)

    payload = {}
    payload["username"] = valid_user_payload["email"]
    payload["password"] = "MySuperPassword123!"

    for _ in range(5):
        login_response = client.post("/users/login", data=payload)
        login_body = login_response.json()

    user = db.query(UserModel).filter(
        UserModel.email == valid_user_payload["email"],
        UserModel.is_active.is_(True)
    ).first()

    assert create_response.status_code == 201
    assert login_response.status_code == 423

    assert len(login_body) == 1

    assert "detail" in login_body

    assert isinstance(login_body["detail"], str)
    
    assert login_body["detail"] == "Account locked"
    assert user.failed_login_attempts == 5
    assert user.locked_until is not None
    assert user.locked_until > datetime.now()

def test_locked_account_cannot_login(client, valid_user_payload):
    create_response = client.post("/users", json=valid_user_payload)

    payload = {}
    payload["username"] = valid_user_payload["email"]
    payload["password"] = "MySuperPassword123!"

    for _ in range(5):
        login_response = client.post("/users/login", data=payload)
        login_body = login_response.json()
    
    payload["password"] = valid_user_payload["password"]
    login_response = client.post("/users/login", data=payload)
    login_body = login_response.json()

    assert create_response.status_code == 201
    assert login_response.status_code == 423

    assert len(login_body) == 1

    assert "detail" in login_body

    assert isinstance(login_body["detail"], str)
    
    assert login_body["detail"] == "Account locked"

def test_lock_expires_and_counter_resets(db, client, valid_user_payload):
    create_response = client.post("/users", json=valid_user_payload)

    payload = {}
    payload["username"] = valid_user_payload["email"]
    payload["password"] = "MySuperPassword123!"

    for _ in range(5):
        login_response = client.post("/users/login", data=payload)
        login_body = login_response.json()
    
    user = db.query(UserModel).filter(
        UserModel.email == valid_user_payload["email"],
        UserModel.is_active.is_(True)
    ).first()

    user.locked_until = (datetime.now() - timedelta(minutes=1))

    db.commit()

    login_response = client.post("/users/login", data=payload)

    db.refresh(user)

    assert create_response.status_code == 201
    assert login_response.status_code == 401

    assert user.failed_login_attempts == 1
    assert user.locked_until is None

def test_successful_login_resets_counter(db, client, valid_user_payload):
    create_response = client.post("/users", json=valid_user_payload)

    payload = {}
    payload["username"] = valid_user_payload["email"]
    payload["password"] = "MySuperPassword123!"

    for _ in range(3):
        login_response = client.post("/users/login", data=payload)
        login_body = login_response.json()
    
    payload["password"] = valid_user_payload["password"]
    login_response = client.post("/users/login", data=payload)
    
    user = db.query(UserModel).filter(
        UserModel.email == valid_user_payload["email"],
        UserModel.is_active.is_(True)
    ).first()

    assert create_response.status_code == 201
    assert login_response.status_code == 200

    assert user.failed_login_attempts == 0
    assert user.locked_until is None

#endregion

#region Test endpoint de prueba /me
def test_get_me_success(client, valid_user_payload):
    create_response = client.post("/users", json=valid_user_payload)

    payload = {}
    payload["username"] = valid_user_payload["email"]
    payload["password"] = valid_user_payload["password"]
    login_response = client.post("/users/login", data=payload)
    login_body = login_response.json()

    token = login_body["access_token"]

    headers = {}
    headers["Authorization"] = f"Bearer {token}"
    me_response = client.get("/users/test/me", headers=headers)
    me_body = me_response.json()
    print(me_body)

    assert create_response.status_code == 201
    assert me_response.status_code == 200

    assert len(me_body) == 4

    assert me_body["name"] == valid_user_payload["name"]
    assert me_body["email"] == valid_user_payload["email"]

def test_get_me_without_token(client, valid_user_payload):
    create_response = client.post("/users", json=valid_user_payload)

    me_response = client.get("/users/test/me")

    assert create_response.status_code == 201
    assert me_response.status_code == 401

def test_get_me_invalid_token(client):
    me_response = client.get("/users/test/me", headers={"Authorization": "Bearer invalid_token"})

    assert me_response.status_code == 401

#endregion