from app.models import UserModel
from app.auth.security import verify_password

def test_create_user_saves_correct_data_in_database(client, db, valid_user_payload):
    response = client.post("/users", json=valid_user_payload)
    body = response.json()

    user = db.query(UserModel).filter(
        UserModel.id == body["id"]
    ).first()

    assert response.status_code == 201

    assert user is not None

    assert user.id == body["id"]
    assert user.name == valid_user_payload["name"]
    assert user.email == valid_user_payload["email"]
    assert user.age == valid_user_payload["age"]
    assert user.is_active is True

    assert valid_user_payload["password"] != user.password_hash
    assert verify_password(valid_user_payload["password"], user.password_hash)

def test_update_user_saves_correct_data_in_database(client, db, created_user, valid_update_payload):
    quantity_before = db.query(UserModel).count()

    response = client.put(f"/users/{created_user['id']}", json=valid_update_payload)

    quantity_after = db.query(UserModel).count()

    user_updated = db.query(UserModel).filter(
        UserModel.id == created_user["id"]
    ).first()

    assert response.status_code == 200

    assert quantity_before == quantity_after

    assert user_updated is not None

    assert user_updated.id == created_user["id"]
    assert user_updated.name == valid_update_payload["name"]
    assert user_updated.email == valid_update_payload["email"]
    assert user_updated.age == valid_update_payload["age"]
    assert user_updated.is_active is True

def test_delete_user_change_state_in_database(client, db, created_user):
    response = client.delete(f"/users/{created_user['id']}")

    user_deleted = db.query(UserModel).filter(
        UserModel.id == created_user["id"]
    ).first()

    assert response.status_code == 204

    assert user_deleted is not None

    assert user_deleted.id == created_user["id"]
    assert user_deleted.name == created_user["name"]
    assert user_deleted.email == created_user["email"]
    assert user_deleted.age == created_user["age"]
    assert user_deleted.is_active is False

def test_patch_user_updates_database(client, db, created_user, patch_user):
    quantity_before = db.query(UserModel).count()

    response = patch_user(id=created_user["id"], name = True)
    body = response.json()

    quantity_after = db.query(UserModel).count()

    user_updated = db.query(UserModel).filter(
        UserModel.id == created_user["id"]
    ).first()

    assert response.status_code == 200

    assert quantity_before == quantity_after

    assert user_updated is not None

    assert user_updated.id == created_user["id"]
    assert user_updated.name == body["name"]
    assert user_updated.email == created_user["email"]
    assert user_updated.age == created_user["age"]
    assert user_updated.is_active is True