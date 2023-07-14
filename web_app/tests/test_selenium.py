from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver


class MySeleniumTests(StaticLiveServerTestCase):
    selenium = None
    # fixtures = ["user-data.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_menu(self):
        self.selenium.get(f"{self.live_server_url}")
        # self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()
        # self.selenium.find_element(By.XPATH, '/html/body/div/div/div[2]/div[2]/div/button').click()
        self.selenium.find_element(By.CLASS_NAME, 'btn.btn-dark.menu-button').click()
