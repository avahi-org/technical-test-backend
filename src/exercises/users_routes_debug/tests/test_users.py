def test_list_users(client):
    assert [u["name"] for u in client.get("/users").json()] == ["Ada", "Linus", "Grace"]


def test_get_user_by_id(client):
    assert client.get("/users/2").json() == {"id": 2, "name": "Linus"}


def test_unknown_user_is_404(client):
    assert client.get("/users/999").status_code == 404


def test_me_defaults_to_user_1(client):
    response = client.get("/users/me")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_me_follows_the_header(client):
    assert client.get("/users/me", headers={"X-User-Id": "3"}).json()["name"] == "Grace"
