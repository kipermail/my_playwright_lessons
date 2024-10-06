from playwright.sync_api import Playwright
from page_objects.test_cases import Test_cases


class App():
    def __init__(self, playwright: Playwright, base_url: str, headless=False, device=None, **kwargs):
        device_config = playwright.devices.get(device)
        if device_config is not None:
            device_config.update(kwargs)
        else:
            device_config = kwargs
        self.browser = playwright.chromium.launch(headless=headless)
        #self.browser = playwright.chromium.launch(headless=headless, devtools=devtools)
        self.context = self.browser.new_context(**device_config )
        self.page = self.context.new_page()
        self.base_url = base_url
        self.test_cases = Test_cases(self.page)
       

    def goto(self, endpoint: str, use_base_url=True):   
        if use_base_url: 
            self.page.goto(self.base_url + endpoint)
        else: 
            self.page.goto(endpoint)

    def navigate_to(self, menu: str):
         self.page.click(f"css=header >> text='{menu}'")


    
    def login(self, login: str, password: str):
        self.page.get_by_label("Username:").fill(login)
        self.page.get_by_label("Password:").fill(password)
        self.page.get_by_role("button", name="Login").click()


    def create_test(self, test_name: str, test_descroption: str):
        self.page.fill("input[name='name']", test_name)
        self.page.fill("textarea[name='description']", test_descroption)
        self.page.click("input[type='submit']")

    def click_menu_button(self):
        self.page.click('.menuBtn')

    def is_menu_button_visible(self):
        return self.page.is_visible('.menuBtn')

    def get_location(self):
        return self.page.text_content('.position')
        

    def close(self):
        self.page.close()
        self.context.close()
        self.browser.close()


