import json

empty_test = {"total": 0, "passed": 0, "failed": 0, "norun": 0}

def test_dashboard_data(desktop_app_auth):
    payload = json.dumps({"total": 0, "passed": 0, "failed": 0, "norun": 0})
    desktop_app_auth.intercept_requests("**/getstat/*", payload)
    desktop_app_auth.refresh_deshboard()
    assert desktop_app_auth.get_total_test_stats() == "0", f"{payload}"
    desktop_app_auth.stop_intercept("**/getstat/*")
