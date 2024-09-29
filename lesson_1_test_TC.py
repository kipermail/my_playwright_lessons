from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, devtools=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto("http://127.0.0.1:8000/login/?next=/")
    page.get_by_label("Username:").fill("alice")
    page.get_by_label("Password:").fill("Qamania123")
    page.get_by_role("button", name="Login").click()
    
    page.get_by_role("link", name="Create new test").click()
    
    page.click("text='Create new test'")
    page.fill("input[name='name']", "hello")
    page.fill("textarea[name='description']", "world")
    page.click("input[type='submit']")

    page.click("text='Test Cases'")
    #page.pause()
    assert page.query_selector("//td[text() ='hello']") is not None

    page.click("//tr[13]/td[9]/button[normalize-space(.)='Delete']")

    page.close()
    context.close()
    browser.close()



def skiped_lesson_1_test_create_TC():
    with sync_playwright() as playwright:
        run(playwright)