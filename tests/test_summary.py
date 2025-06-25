from tests.conftest import get_admin_token

def test_view_summary(client, admin_credentials):
    token = get_admin_token(client, admin_credentials)
    period = client.post("/api/v1/admin/payroll-period",
                         json={"start_date": "2025-06-01", "end_date": "2025-06-30"},
                         headers={"Authorization": f"Bearer {token}"}).json()
    client.post(f"/api/v1/employee/payroll-run/{period['id']}", headers={"Authorization": f"Bearer {token}"})
    res = client.get(f"/api/v1/admin/payroll-summary/{period['id']}", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
