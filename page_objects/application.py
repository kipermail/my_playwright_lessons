from playwright.sync_api import Playwright


class App():
    def __init__(self, playwright: Playwright):
        self.browser = playwright.chromium.launch(headless=False, devtools=True)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.goto("http://127.0.0.1:8000/login/?next=/")

    
    def login(self):
        self.page.get_by_label("Username:").fill("alice")
        self.page.get_by_label("Password:").fill("Qamania123")
        self.page.get_by_role("button", name="Login").click()


    def create_test(self):
        self.page.click("text='Create new test'")
        self.page.fill("input[name='name']", "hello")
        self.page.fill("textarea[name='description']", "world")
        self.page.click("input[type='submit']")


    def open_tests(self):
        self.page.click("text='Test Cases'")


    def check_test_created(self):
        self.page.query_selector("//td[text() ='hello']") is not None


    def delete_test(self):    
        self.page.click("//tr[13]/td[9]/button[normalize-space(.)='Delete']")


    def close(self):
        self.page.close()
        self.context.close()
        self.browser.close()


