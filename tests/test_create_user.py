def test_create_user_success(client):
    payload = {
        "name": "Alex",
        "email": "alex@gmail.com",
        "age": 25
    }

    response = client.post("/users", json=payload)
    
    assert response.status_code == 200
    assert response.json() == {"message": "User received"}

def test_create_user_name_too_short(client):
    payload = {
        "name": "A",
        "email": "alex@gmail.com",
        "age": 25
    }

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