from pytest import mark
from playwright.sync_api import Page
from page_objects.application import App
from page_objects.demo_pages import DemoPages

@mark.skip
def test_wait_more_10_sec(desktop_app_auth):
    desktop_app_auth.navigate_to("Demo pages")
    desktop_app_auth.demo_pages.open_page_after_wait(11)
    assert desktop_app_auth.demo_pages.check_wait_page()

@mark.skip
def test_ajax(desktop_app_auth):
    desktop_app_auth.navigate_to("Demo pages")
    desktop_app_auth.demo_pages.open_page_and_wait_ajax(2)
    assert desktop_app_auth.demo_pages.get_ajax_responce_count() == 2

@mark.skip
def test_handlers(desktop_app_auth):
    desktop_app_auth.navigate_to("Demo pages")
    desktop_app_auth.demo_pages.click_new_page_button(ctrl_key=False)
    desktop_app_auth.demo_pages.inject_js()
    desktop_app_auth.navigate_to("Test Cases")
    assert desktop_app_auth.test_cases.check_test_exists("Check new test")
