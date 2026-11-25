def _token(client, username="john_doe", password="password"):
    return client.post("/token", data={"username": username, "password": password})


def test_health(client):
    assert client.get("/").json() == {"message": "Hello, World!"}


def test_login_returns_bearer_token(client):
    response = _token(client)
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_login_rejects_wrong_password(client):
    assert _token(client, password="nope").status_code == 401


def test_me_without_token_is_unauthorized(client):
    assert client.get("/me").status_code == 401


def test_me_returns_the_logged_in_user(client):
    token = _token(client).json()["access_token"]
    response = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"username": "john_doe"}
