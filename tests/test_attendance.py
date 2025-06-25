import datetime
from tests.conftest import get_token

def test_valid_attendance(client, user_credentials):
    token = get_token(client, user_credentials)
    today = datetime.date.today().isoformat()

    res = client.post("/api/v1/employee/attendance", json={"date": today}, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["date"] == today

def test_invalid_attendance_weekend(client, user_credentials):
    token = get_token(client, user_credentials)
    saturday = "2025-06-28"  # Adjust ke hari Sabtu
    res = client.post("/api/v1/employee/attendance", json={"date": saturday}, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 400
