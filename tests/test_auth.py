def test_register_and_login(client, user_credentials):
    res = client.post("/api/v1/employee/register", json=user_credentials)
    assert res.status_code == 200

    res = client.post("/api/v1/employee/login", data=user_credentials)
    assert res.status_code == 200
    assert "access_token" in res.json()
