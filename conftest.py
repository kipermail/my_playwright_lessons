import os
import json
import pytest
import allure
import logging
from settings import *
from pytest import fixture, hookimpl
from playwright.sync_api import sync_playwright
from page_objects.application import App
from helpers.web_service import WebService
from helpers.db import Database


@fixture(scope='session', autouse=True)
def precondition(request):
    logging.info('Precondition started')
    base_url = request.config.getoption("--base_url")
    tcm = request.config.getini('tcm_report')
    secure = request.config.getoption("--secure")
    config = load_config(secure)
    yield
    logging.info('Postcondition started')
    if tcm == 'True':
        web = WebService(base_url)
        web.login(**config['users']['userRole3'])
        for test in request.node.items:
            if len(test.own_markers) > 0:
                if test.own_markers[0].name == "test_id":
                    if test.result_call.passed:
                        web.report_test_execute(test.own_markers[0].args[0], "PASS")
                    if test.result_call.failed:
                        web.report_test_execute(test.own_markers[0].args[0], "FAIL")




@fixture(scope="session")
def get_web_service(request):
    base_url = request.config.getoption("--base_url")
    secure = request.config.getoption("--secure")
    config = load_config(secure)
    web_service = WebService(base_url)
    web_service.login(**config['users']['userRole1'])
    yield web_service
    web_service.close() 

@fixture(scope="session")
def get_db(request):
    path = request.config.getini("db_path")
    db = Database(path)
    yield db
    db.close()

@fixture(scope="session")
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright

#@fixture(params = ["chromium", "firefox", "webkit"], ids = ["chromium", "firefox", "webkit"])
@fixture(scope="session", params = ["chromium"], ids = ["chromium"])
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

@fixture(scope="session")
def desktop_app(get_browser, request):
    base_url = request.config.getoption("--base_url")
    #base_url = request.config.getini("base_url")
    app = App(get_browser, base_url=base_url, **BROWSER_OPTIONS )
    app.goto("/")
    yield app
    app.close()       

@fixture(scope="session")
def desktop_app_auth(desktop_app, request):
    secure = request.config.getoption("--secure")
    config = load_config(secure)
    app = desktop_app
    app.goto("/login")
    app.login(**config['users']['userRole1'])
    yield app    

@fixture(scope="session")
def desktop_app_bob(get_browser, request):
    base_url = request.config.getini('base_url')
    secure = request.config.getoption("--secure")
    config = load_config(secure)
    app = App(get_browser, base_url=base_url, **BROWSER_OPTIONS)
    app.goto("/login")
    app.login(**config['users']['userRole2'])
    yield app     

#@fixture(params = ["iPhone 12 Pro", "iPhone 14", "Pixel 7"], ids = ["iPhone 12 Pro", "iPhone 14", "Pixel 7"]   )
@fixture(params = ["iPhone 12 Pro"], ids = ["iPhone 12 Pro"]   )
def mobile_app(get_playwright, get_browser, request):
    if os.environ.get("PWBROWSER") == "firefox":
        pytest.skip("Browser is not supported for mobile tests")
    base_url = request.config.getoption("--base_url")
    #base_url = request.config.getini("base_url")
    device = request.param
    device_config = get_playwright.devices.get(device)
    if device_config is not None:
            device_config.update(BROWSER_OPTIONS)
    else:
            device_config = BROWSER_OPTIONS
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
    app.login(**config['users']['userRole1'])
    yield app    

@hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    #result.when == 'setup'>>'call'>>'teardown'
    setattr(item, f'result_{result.when}', result)

@fixture(scope="function", autouse=True)
def make_screenshots(request):
    yield
    if request.node.result_call.failed:
        for arg in request.node.funcargs.values():
            if isinstance(arg, App):
                allure.attach(body=arg.page.screenshot(),
                              name="screenshot",
                              attachment_type=allure.attachment_type.PNG)   


def pytest_addoption(parser):
    parser.addoption("--secure", action="store", default="secure.json")
    # parser.addoption("--mdevice", action="store", default="")
    # parser.addoption("--mbrowser", action="store", default="chromium")
    parser.addoption("--base_url", action="store", default="http://127.0.0.1:8000")
    parser.addini("headless", help="Run browser in headless mode", default="True")
    #parser.addini("base_url", help="Base url of site under test", default="http://127.0.0.1:8000")
    parser.addini("db_path", help="path to sqlite db file", default= "/Users/medstar/Documents/projects/Python/TestMe-TCM-main/db.sqlite3")
    parser.addini('tcm_report', help='report test results to tcm', default='False')


def load_config(file):
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(config_file) as cfg:
        return json.loads(cfg.read())
