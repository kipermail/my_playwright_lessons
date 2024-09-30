from pytest import mark

test_data = [
    ("hello", "world"),
    ("hello", ""),
    ("123", "world123"),
]

@mark.parametrize("test_name, description", test_data, ids=["general test", "empty description", "number in name"])
def test_new_testcase(desktop_app_auth, test_name, description):
    desktop_app_auth.navigate_to("Create new test")
    desktop_app_auth.create_test(test_name, description)
    desktop_app_auth.navigate_to("Test Cases")
    assert desktop_app_auth.test_cases.check_test_exists(test_name)
    desktop_app_auth.test_cases.delete_test_by_name(test_name)
    #desktop_app.close()

