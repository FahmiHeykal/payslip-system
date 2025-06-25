from tests.conftest import get_token

def test_view_payslip(client, user_credentials):
    token = get_token(client, user_credentials)
    res = client.get("/api/v1/employee/payslips", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert isinstance(res.json(), list)
