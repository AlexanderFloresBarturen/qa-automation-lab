from datetime import datetime, timedelta
import pytest
from unittest.mock import patch, ANY

from app.models.token_model import PasswordResetTokenModel
from app.models.user_model import UserModel
from app.services.email_service import send_password_reset_email
from tests.helpers import assert_reset_password_invalid_token_response

#region forgot-password
def test_forgot_password_success(db, client, created_user):
    fp_response = client.post("/users/forgot-password", json={"email": created_user["email"]})
    fp_body = fp_response.json()

    token = db.query(PasswordResetTokenModel).filter(
        PasswordResetTokenModel.user_id == created_user["id"]
    ).first()

    assert fp_response.status_code == 200
    
    assert len(fp_body) == 2

    assert "message" in fp_body
    assert "token" in fp_body

    assert isinstance(fp_body["message"], str)
    assert isinstance(fp_body["token"], str)

    assert fp_body["message"] == "Recovery token generated"
    assert fp_body["token"] == token.token
    assert token.user_id == created_user["id"]
    assert token.expires_at is not None
    assert token.used is False

def test_forgot_password_nonexisting_email(db, client):
    quantity_before = db.query(PasswordResetTokenModel).count()
    
    fp_response = client.post("/users/forgot-password", json={"email": "email@email.com"})
    fp_body = fp_response.json()

    quantity_after = db.query(PasswordResetTokenModel).count()

    assert fp_response.status_code == 200

    assert len(fp_body) == 2

    assert "message" in fp_body
    assert "token" in fp_body

    assert isinstance(fp_body["message"], str)

    assert fp_body["message"] == "If the account exists, a recovery token has been generated"
    assert fp_body["token"] is None
    assert quantity_before == quantity_after

def test_forgot_password_invalidates_previous_token(db, client, created_user):
    for _ in range(3):
        client.post("/users/forgot-password", json={"email": created_user["email"]})
    
    tokens = db.query(PasswordResetTokenModel).filter(
        PasswordResetTokenModel.user_id == created_user["id"]
    ).order_by(PasswordResetTokenModel.created_at).all()

    assert len(tokens) == 3

    total_tokens = len(tokens)
    for index, token in enumerate(tokens):
        if index == total_tokens -1:
            assert token.used is False
        else:
            assert token.used is True

#region Mocks
"""
Se parchea donde la función es utilizada -> app.routes.users 
porque en esa ruta es donde forgot-password() llama a la función
send_password_reset_email()
"""
@patch("app.routes.users.send_password_reset_email")
def test_forgot_password_calls_email_service(mock_send_email, client, created_user):
    fp_response = client.post("/users/forgot-password", json={"email": created_user["email"]})

    assert fp_response.status_code == 200

    mock_send_email.assert_called_once()
    mock_send_email.assert_called_once_with(email=created_user["email"], token=ANY)

@patch("app.routes.users.send_password_reset_email")
def test_forgot_password_email_service_unavailable(mock_send_email, client, created_user):
    mock_send_email.return_value = False

    fp_response = client.post("/users/forgot-password", json={"email": created_user["email"]})
    fp_body = fp_response.json()

    assert fp_response.status_code == 500

    assert len(fp_body) == 1

    assert "detail" in fp_body

    assert isinstance(fp_body["detail"], str)

    assert fp_body["detail"] == "Email service unavailable"

    mock_send_email.assert_called_once()
    mock_send_email.assert_called_once_with(email=created_user["email"], token=ANY)

@patch("app.routes.users.send_password_reset_email", wraps=send_password_reset_email)
def test_forgot_password_spy_email_service(spy_send_email, client, created_user):
    fp_response = client.post("/users/forgot-password", json={"email": created_user["email"]})

    assert fp_response.status_code == 200

    spy_send_email.assert_called_once()

    assert spy_send_email.call_count == 1
    assert spy_send_email.call_args.kwargs["email"] == created_user["email"]

@patch("app.routes.users.send_password_reset_email")
def test_forgot_password_email_service_exception(mock_send_email, client, created_user):
    mock_send_email.side_effect = ConnectionError("SMTP server unavailable")

    fp_response = client.post("/users/forgot-password", json={"email": created_user["email"]})
    fp_body = fp_response.json()

    assert fp_response.status_code == 500

    assert len(fp_body) == 1

    assert "detail" in fp_body

    assert isinstance(fp_body["detail"], str)

    assert fp_body["detail"] == "Email service unavailable"

#endregion

"""
Monkeypatch
Su objetivo es reemplazar (durante la ejecución) funciones, constantes, variables de entorno, etc.
"""
def test_forgot_password_monkeypatch_email_failure(monkeypatch, client, created_user):
    def fake_email_service(email: str, token:str):
        # print("SOY FAKE")
        return False
    
    monkeypatch.setattr("app.routes.users.send_password_reset_email", fake_email_service)

    fp_response = client.post("/users/forgot-password", json={"email": created_user["email"]})
    fp_body = fp_response.json()

    assert fp_response.status_code == 500

    assert len(fp_body) == 1

    assert "detail" in fp_body

    assert isinstance(fp_body["detail"], str)

    assert fp_body["detail"] == "Email service unavailable"

#endregion

#region reset-password
def test_reset_password_success(db, client, user_reset_password_payload):
    rp_payload = user_reset_password_payload()
    rp_response = client.post("/users/reset-password", json= rp_payload)
    rp_body = rp_response.json()

    token = db.query(PasswordResetTokenModel).filter(
        PasswordResetTokenModel.token == rp_payload["token"]
    ).first()

    assert rp_response.status_code == 200

    assert len(rp_body) == 1
    
    assert "message" in rp_body

    assert isinstance(rp_body["message"], str)

    assert rp_body["message"] == "Password successfully reset"
    assert token.used is True

def test_reset_password_invalid_token(client):
    rp_payload = {
        "token": "invalid_token",
        "new_password": "NewPassword123!"
    }

    rp_response = client.post("/users/reset-password", json= rp_payload)
    rp_body = rp_response.json()

    assert rp_response.status_code == 400

    assert_reset_password_invalid_token_response(rp_body)

def test_reset_password_used_token(client, user_reset_password_payload):
    rp_payload = user_reset_password_payload()
    rp_response_one = client.post("/users/reset-password", json= rp_payload)
    rp_response_two = client.post("/users/reset-password", json= rp_payload)
    rp_body = rp_response_two.json()

    assert rp_response_one.status_code == 200
    assert rp_response_two.status_code == 400

    assert_reset_password_invalid_token_response(rp_body)

def test_reset_password_expired_token(db, client, user_reset_password_payload):
    rp_payload = user_reset_password_payload()

    token = db.query(PasswordResetTokenModel).filter(
        PasswordResetTokenModel.token == rp_payload["token"]
    ).first()

    token.expires_at = (datetime.now() - timedelta(minutes=1))
    db.commit()

    rp_response = client.post("/users/reset-password", json= rp_payload)
    rp_body = rp_response.json()

    assert rp_response.status_code == 400

    assert_reset_password_invalid_token_response(rp_body)

@pytest.mark.parametrize(
        "password, type, error_message",
        [
            ("password123!", "value_error", "The password must contain at least one uppercase letter"),
            ("PASSWORD123!", "value_error", "The password must contain at least one lowercase letter"),
            ("Password!!!", "value_error", "The password must contain at least one number"),
            ("Password123", "value_error", "The password must contain at least one special character"),
            ("Pass1!", "string_too_short", "String should have at least 8 characters")
        ]
)
def test_reset_password_invalid_password(client, user_reset_password_payload, password, type, error_message):
    rp_payload = user_reset_password_payload(password= password)
    rp_response = client.post("/users/reset-password", json= rp_payload)
    rp_body = rp_response.json()

    assert rp_response.status_code == 422

    assert "detail" in rp_body
    assert "loc" in rp_body["detail"][0]
    assert "type" in rp_body["detail"][0]
    assert "msg" in rp_body["detail"][0]

    assert rp_body["detail"][0]["loc"] == ["body", "new_password"]
    assert rp_body["detail"][0]["type"] == type
    assert error_message in rp_body["detail"][0]["msg"]

def test_reset_password_updates_hash(db, client, user_reset_password_payload):
    rp_payload = user_reset_password_payload()

    token = db.query(PasswordResetTokenModel).filter(
        PasswordResetTokenModel.token == rp_payload["token"]
    ).first()

    old_hash = token.user.password_hash

    rp_response = client.post("/users/reset-password", json= rp_payload)
    
    db.refresh(token.user)

    new_hash = token.user.password_hash

    assert rp_response.status_code == 200

    assert old_hash != new_hash

def test_reset_password_unlocks_account(db, client, valid_user_payload):
    create_response = client.post("/users", json=valid_user_payload)

    login_payload = {}
    login_payload["username"] = valid_user_payload["email"]
    login_payload["password"] = "MySuperPassword123!"

    for _ in range(5):
        login_response = client.post("/users/login", data=login_payload)
    
    fp_response = client.post("/users/forgot-password", json={"email": valid_user_payload["email"]})
    fp_body = fp_response.json()

    rp_payload = {
        "token": fp_body["token"],
        "new_password": "NewPassword123!"
    }
    rp_response = client.post("/users/reset-password", json= rp_payload)

    user = db.query(UserModel).filter(
        UserModel.email == valid_user_payload["email"]
    ).first()

    assert create_response.status_code == 201
    assert login_response.status_code == 423
    assert fp_response.status_code == 200
    assert rp_response.status_code == 200

    assert user.failed_login_attempts == 0
    assert user.locked_until is None

#endregion

#region flujo completo
def test_reset_password_changes_login_credentials(client, valid_user_payload):
    create_response = client.post("/users", json=valid_user_payload)

    fp_response = client.post("/users/forgot-password", json={"email": valid_user_payload["email"]})
    fp_body = fp_response.json()

    new_password = "NewPassword123!"
    rp_payload = {
        "token": fp_body["token"],
        "new_password": new_password
    }
    rp_response = client.post("/users/reset-password", json= rp_payload)

    login_payload_old_pwd = {}
    login_payload_old_pwd["username"] = valid_user_payload["email"]
    login_payload_old_pwd["password"] = valid_user_payload["password"]
    login_response_old_pwd = client.post("/users/login", data=login_payload_old_pwd)

    login_payload_new_pwd = {}
    login_payload_new_pwd["username"] = valid_user_payload["email"]
    login_payload_new_pwd["password"] = new_password
    login_response_new_pwd = client.post("/users/login", data=login_payload_new_pwd)

    assert create_response.status_code == 201
    assert fp_response.status_code == 200
    assert rp_response.status_code == 200
    assert login_response_old_pwd.status_code == 401
    assert login_response_new_pwd.status_code == 200

#endregion