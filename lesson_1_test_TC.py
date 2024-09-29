from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://127.0.0.1:8000/login/?next=/")
    page.get_by_label("Username:").click()
    page.get_by_label("Username:").fill("alice")
    page.get_by_label("Password:").click()
    page.get_by_label("Password:").fill("Qamania123")
    page.get_by_role("button", name="Login").click()
    page.get_by_role("link", name="Create new test").click()
    page.locator("#id_name").click()
    page.locator("#id_name").fill("hello")
    page.get_by_label("Test description").click()
    page.get_by_label("Test description").fill("world")
    page.get_by_role("button", name="Create").click()
    page.get_by_role("link", name="Test Cases").click()

    assert page.query_selector("//td[text() ='hello']") is not None

    page.get_by_role("row", name="hello world alice Norun None PASS FAIL Details Delete").get_by_role("button").nth(3).click()

    page.close()

    # ---------------------
    


    context.close()
    browser.close()

# def test_createTC():
with sync_playwright() as playwright:
    run(playwright)
