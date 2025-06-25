from tests.conftest import get_admin_token

def test_create_payroll_period(client, admin_credentials):
    token = get_admin_token(client, admin_credentials)
    res = client.post("/api/v1/admin/payroll-period",
                      json={"start_date": "2025-06-01", "end_date": "2025-06-30"},
                      headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200

def test_run_payroll(client, admin_credentials):
    token = get_admin_token(client, admin_credentials)
    period = client.post("/api/v1/admin/payroll-period", json={"start_date": "2025-06-01", "end_date": "2025-06-30"}, headers={"Authorization": f"Bearer {token}"}).json()
    res = client.post(f"/api/v1/employee/payroll-run/{period['id']}", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
