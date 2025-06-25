from tests.conftest import get_token

def test_valid_overtime(client, user_credentials):
    token = get_token(client, user_credentials)
    res = client.post("/api/v1/employee/overtime", json={"date": "2025-06-25", "hours": 3}, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200

def test_invalid_overtime_too_many_hours(client, user_credentials):
    token = get_token(client, user_credentials)
    res = client.post("/api/v1/employee/overtime", json={"date": "2025-06-25", "hours": 13}, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 422 
