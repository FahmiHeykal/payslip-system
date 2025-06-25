from tests.conftest import get_token

def test_reimbursement(client, user_credentials):
    token = get_token(client, user_credentials)
    payload = {"date": "2025-06-20", "amount": 200000, "description": "Transport"}
    res = client.post("/api/v1/employee/reimbursement", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
