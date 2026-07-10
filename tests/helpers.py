def assert_valid_user_response(body):
    assert len(body) == 4

    assert "id" in body
    assert "name" in body
    assert "email" in body
    assert "age" in body

    assert isinstance(body["id"], int)
    assert isinstance(body["name"], str)
    assert isinstance(body["email"], str)
    assert isinstance(body["age"], int)

    assert body["id"] > 0


def assert_user_not_found_response(body):
    assert len(body) == 1

    assert "detail" in body

    assert isinstance(body["detail"], str)

    assert body["detail"] == "User not found"


def assert_duplicate_email_response(body):
    assert len(body) == 1

    assert "detail" in body

    assert isinstance(body["detail"], str)

    assert body["detail"] == "Email already exists"


def assert_not_found_response(body):
    assert len(body) == 1

    assert "detail" in body

    assert isinstance(body["detail"], str)

    assert body["detail"] == "Not Found"


def assert_not_authenticated_response(body):
    assert len(body) == 1

    assert "detail" in body

    assert isinstance(body["detail"], str)

    assert body["detail"] == "Not authenticated"


# Usando en los tokens que se envían a los endpoints protegidos
def assert_invalid_token_response(body):
    assert len(body) == 1

    assert "detail" in body

    assert isinstance(body["detail"], str)

    assert body["detail"] == "Could not validate credentials"


# Usado en los tokens de cambio de contraseña
def assert_reset_password_invalid_token_response(body):
    assert len(body) == 1

    assert "detail" in body

    assert isinstance(body["detail"], str)

    assert body["detail"] == "Invalid token"
