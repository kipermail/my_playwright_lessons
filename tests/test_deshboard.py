import json
import allure
from pytest import mark

empty_test = {"total": 0, "passed": 0, "failed": 0, "norun": 0}

@mark.skip
@allure.title("Test updating deshboard params" )
def test_dashboard_data(desktop_app_auth):
    payload = json.dumps({"total": 0, "passed": 0, "failed": 0, "norun": 0})
    desktop_app_auth.intercept_requests("**/getstat/*", payload)
    desktop_app_auth.refresh_deshboard()
    assert desktop_app_auth.get_total_test_stats() == "0", f"{payload}"
    desktop_app_auth.stop_intercept("**/getstat/*")

@allure.title("Test multiple user roles" )
def test_multiple_roles(desktop_app_auth, desktop_app_bob):
    alice = desktop_app_auth
    bob = desktop_app_bob
    before = alice.get_total_test_stats()
    bob.navigate_to("Create new test")
    bob.create_test("role_test", "role_test_description")
    alice.refresh_deshboard()
    after = alice.get_total_test_stats()
    bob.navigate_to("Test Cases")
    bob.test_cases.delete_test_by_name("role_test")
    #get_db.delete_test_case('test by bob')
    assert int(after) == int(before) + 1, "Bob not add test to Alice"

    