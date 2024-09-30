from pytest import fixture
from playwright.sync_api import sync_playwright
from page_objects.application import App

@fixture
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright


@fixture
def desktop_app(get_playwright, request):
    #base_url = request.config.getoption("--base_url")
    base_url = request.config.getini("base_url")
    app = App(get_playwright, base_url=base_url)
    app.goto("/")
    yield app
    app.close()       


@fixture
def desktop_app_auth(desktop_app):
    app = desktop_app
    app.goto("/login")
    app.login("alice", "Qamania123")
    yield app     
    

def pytest_addoption(parser):
    #parser.addoption("--base_url", action="store", default="http://127.0.0.1:8000")
    parser.addini("base_url", help="base url of tested site", default="http://127.0.0.1:8000") 