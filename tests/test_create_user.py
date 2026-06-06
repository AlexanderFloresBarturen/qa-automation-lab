def test_create_user_success(client, valid_user_payload):
    response = client.post("/users", json=valid_user_payload)
    body = response.json()
    
    assert response.status_code == 201

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
    assert body["name"] == valid_user_payload["name"]
    assert body["email"] == valid_user_payload["email"]
    assert body["age"] == valid_user_payload["age"]
    


def test_create_user_name_too_short(client, valid_user_payload):
    payload = valid_user_payload.copy()
    payload["name"] = "A"

    response = client.post("/users", json=payload)
    body = response.json()

    assert response.status_code == 422
    assert "detail" in body
    assert "type" in body["detail"][0]
    assert body["detail"][0]["type"] == "string_too_short"
    assert "loc" in body["detail"][0]
    assert body["detail"][0]["loc"] == ["body", "name"]

def test_create_user_missing_age(client):
    payload = {
        "name": "Alex",
        "email": "alex@gmail.com"
    }

    response = client.post("/users", json=payload)
    body = response.json()

    assert response.status_code == 422
    assert "detail" in body
    assert "type" in body["detail"][0]
    assert body["detail"][0]["type"] == "missing"
    assert "loc" in body["detail"][0]
    assert body["detail"][0]["loc"] == ["body", "age"]

def test_create_user_empty_payload(client):
    payload = {}

    response = client.post("/users", json=payload)
    body = response.json()

    assert response.status_code == 422
    assert "detail" in body
    assert "type" in body["detail"][0]
    assert "type" in body["detail"][1]
    assert "type" in body["detail"][2]
    assert body["detail"][0]["type"] == "missing"
    assert body["detail"][1]["type"] == "missing"
    assert body["detail"][2]["type"] == "missing"
    assert "loc" in body["detail"][0]
    assert "loc" in body["detail"][1]
    assert "loc" in body["detail"][2]
    assert body["detail"][0]["loc"] == ["body", "name"]
    assert body["detail"][1]["loc"] == ["body", "email"]
    assert body["detail"][2]["loc"] == ["body", "age"]