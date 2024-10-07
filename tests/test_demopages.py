from pytest import mark
from playwright.sync_api import Page
from page_objects.application import App
from page_objects.demo_pages import DemoPages


def test_wait_more_10_sec(desktop_app_auth):
    desktop_app_auth.navigate_to("Demo pages")
    desktop_app_auth.demo_pages.open_page_after_wait(11)
    assert desktop_app_auth.demo_pages.check_wait_page()

def test_ajax(desktop_app_auth):
    desktop_app_auth.navigate_to("Demo pages")
    desktop_app_auth.demo_pages.open_page_and_wait_ajax(6)
    assert desktop_app_auth.demo_pages.get_ajax_responce_count() == 6
