import os
import json
import pytest
from settings import *
from pytest import fixture
from playwright.sync_api import sync_playwright
from page_objects.application import App

@fixture
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright


@fixture(params = ["chromium", "firefox", "webkit"], ids = ["chromium", "firefox", "webkit"])
def get_browser(get_playwright, request):
    browser = request.param
    os.environ['PWBROWSER'] = browser
    headless = request.config.getini("headless")
    if headless == "True":
        headless = True
    else:
        headless = False

    if browser == "chromium":
        brows = get_playwright.chromium.launch(headless=headless)
    elif browser == "firefox":
        brows = get_playwright.firefox.launch(headless=headless)
    elif browser == "webkit":
        brows = get_playwright.webkit.launch(headless=headless)
    else:
        assert False, "unsupported browser type"
    
    yield brows
    brows.close()
    del os.environ['PWBROWSER']

@fixture
def desktop_app(get_browser, request):
    base_url = request.config.getoption("--base_url")
    #base_url = request.config.getini("base_url")
    app = App(get_browser, base_url=base_url, **BROWSER_OPTIONS )
    app.goto("/")
    yield app
    app.close()       


@fixture
def desktop_app_auth(desktop_app, request):
    secure = request.config.getoption("--secure")
    config = load_config(secure)
    app = desktop_app
    app.goto("/login")
    app.login(**config)
    yield app     
    

@fixture(params = ["iPhone 12 Pro", "iPhone 14", "Pixel 7"], ids = ["iPhone 12 Pro", "iPhone 14", "Pixel 7"]   )
def mobile_app(get_playwright, get_browser, request):
    if os.environ.get("PWBROWSER") == "firefox":
        pytest.skip("Browser is not supported for mobile tests")
    base_url = request.config.getoption("--base_url")
    device = request.param
    device_config = get_playwright.devices.get(device)
    if device_config is not None:
            device_config.update(BROWSER_OPTIONS)
    else:
            device_config = BROWSER_OPTIONS
    #base_url = request.config.getini("base_url")
    app = App(get_browser, base_url=base_url, **device_config)
    app.goto("/")
    yield app
    app.close()       

@fixture
def mobile_app_auth(mobile_app, request):
    secure = request.config.getoption("--secure")
    config = load_config(secure)
    app = mobile_app
    app.goto("/login")
    app.login(**config)
    yield app    


def pytest_addoption(parser):
    parser.addoption("--base_url", action="store", default="http://127.0.0.1:8000")
    parser.addoption("--secure", action="store", default="secure.json")
    parser.addoption("--mdevice", action="store", default="")
    parser.addoption("--mbrowser", action="store", default="chromium")
    parser.addini("headless", help="Run browser in headless mode", default="True")
    parser.addini("base_url", help="Base url of site under test", default="http://127.0.0.1:8000")
    


def load_config(file):
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(config_file) as cfg:
        return json.loads(cfg.read())
