import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.expected_conditions as EC


class IntegrationTests(StaticLiveServerTestCase):
    """
    Class to perform integration tests on a Django website using Selenium.

    This class uses Selenium WebDriver to run tests on live server, checking if website elements function as expected.

    ...

    Attributes
    ----------
    selenium : WebDriver
        An instance of Selenium WebDriver.

    ...

    Methods
    -------
    setUpClass() -> None:
        Class method called before all the test cases are run. Initializes Selenium WebDriver and sets implicit wait.

    tearDownClass() -> None:
        Class method called after all the tests are run. Quits the Selenium WebDriver.

    test_menu() -> None:
        Test to check the functionality of the top dropdown menu in the website.

    test_bottom() -> None:
        Test to check the functionality of the bottom offcanvas in the website.
    """

    selenium = None

    @classmethod
    def setUpClass(cls):
        """
        Class method that is called before tests in an individual class are run.
        Initializes Selenium WebDriver and sets an implicit wait.
        """

        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        """
        Class method that is called after all tests in an individual class have run.
        Quits the Selenium WebDriver.
        """

        cls.selenium.quit()
        super().tearDownClass()

    def test_offcanvas_top(self):
        """
        Tests the functionality of the top dropdown menu in the website.
        Checks whether the dropdown menu appears and disappears as expected when clicked.
        """

        self.selenium.get(f"{self.live_server_url}")

        dropdown_menu = self.selenium.find_element(By.XPATH, '//*[@id="offcanvasTop"]')

        # click on dropdown menu button, wait for it to appear, and check if it has updated its class
        self.selenium.find_element(By.CSS_SELECTOR, 'button.btn.btn-dark.menu-button').click()
        time.sleep(1)
        self.assertEquals(dropdown_menu.get_attribute("class"), "offcanvas offcanvas-top show")

        # click on dropdown menu close button, wait for it to disappear, and check if it has updated its class
        WebDriverWait(self, 10).until(EC.element_to_be_clickable(
            self.selenium.find_element(By.CSS_SELECTOR, 'button.btn-close'))).click()
        time.sleep(1)
        self.assertEquals(dropdown_menu.get_attribute("class"), "offcanvas offcanvas-top")

    def test_offcanvas_bottom(self):
        """
        Tests the functionality of the bottom offcanvas menu in the website.
        Checks whether it shows and hides correctly when interacted with.
        """

        self.selenium.get(f"{self.live_server_url}")

        # click on bottom offcanvas menu button, wait for it to appear, and check if it has updated its class
        self.selenium.find_element(By.CSS_SELECTOR, '.offcanvas-button').click()
        time.sleep(1)
        self.assertEqual(self.selenium.find_element(By.XPATH, '//*[@id="offcanvasBottom"]').get_attribute('class'),
                         "offcanvas offcanvas-bottom show")

        # calculate point in top 20% of window - needed to make bottom menu disappear
        window_size = self.selenium.get_window_size()
        x_coordinate = window_size["width"] / 2
        y_coordinate = window_size["height"] / 5

        # click on previously defined point to close bottom offcanvas menu and wait for it to disappear
        actions = ActionChains(self.selenium)
        actions.move_by_offset(x_coordinate, y_coordinate).click().perform()
        time.sleep(1)
        # check it disappeared by verifying its class has been updated
        self.assertEqual(
            self.selenium.find_element(By.XPATH, '//*[@id="offcanvasBottom"]').get_attribute('class'),
            "offcanvas offcanvas-bottom")
