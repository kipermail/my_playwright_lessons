import allure
from pytest import mark

ddt = {
    "argnames": "test_name, description",
    "argvalues": [
    ("hello", "world"),
    ("hello", ""),
    ("123", "world123") ],
    "ids" : ["general test", "empty description", "number in name"],
}


@mark.skip
@mark.parametrize(**ddt)
@allure.title("Creating new test case")
def test_new_testcase(desktop_app_auth, test_name, description, get_db):
    tests = get_db.list_test_cases()
    desktop_app_auth.navigate_to("Create new test")
    desktop_app_auth.create_test(test_name, description)
    desktop_app_auth.navigate_to("Test Cases")
    assert len(get_db.list_test_cases()) == len(tests) + 1, 'Test case was not created'
    assert desktop_app_auth.test_cases.check_test_exists(test_name), f'No test case with name {test_name}'
    get_db.delete_test_case(test_name)
    #desktop_app_auth.test_cases.delete_test_by_name(test_name)
    #desktop_app.close()

#@mark.skip
@allure.title("Test case dos not exist in the list")
def test_testcase_does_not_exist(desktop_app_auth):
    desktop_app_auth.navigate_to("Test Cases")
    assert not desktop_app_auth.test_cases.check_test_exists("123321")

@mark.skip
@allure.title("Deleting test case from list")
def test_delete_test_case(desktop_app_auth, get_web_service):
        test_name = "Test for deletion"
        get_web_service.create_test(test_name, "Delete me pls")
        desktop_app_auth.navigate_to("Test Cases")
        assert desktop_app_auth.test_cases.check_test_exists(test_name)
        desktop_app_auth.test_cases.delete_test_by_name(test_name)
        desktop_app_auth.test_cases.check_test_exists(test_name)
        assert not desktop_app_auth.test_cases.check_test_exists(test_name)