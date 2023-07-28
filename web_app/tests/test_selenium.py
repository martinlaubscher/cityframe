import os
import sys
import time

current_path = os.path.dirname(os.path.abspath(__file__))
cityframe_path = os.path.dirname(os.path.dirname(current_path))
sys.path.append(cityframe_path)

import datetime
import re
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from dateutil import tz
from datetime import datetime, timedelta
from data.database.data_population_scripts import update_weather_fc
from data import machine_learning_app


class ElementHasValue:
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        return element.get_attribute("value") != ""


class ElementHasClass(object):
    def __init__(self, locator, css_class):
        self.locator = locator
        self.css_class = css_class

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        # if self.css_class in element.get_attribute("class"):
        #     return element
        # else:
        #     return False
        return self.css_class == element.get_attribute("class")


class TextMatchesPattern(object):
    def __init__(self, locator, pattern):
        self.locator = locator
        self.pattern = pattern

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if bool(re.match(self.pattern, element.text)):
            return element
        else:
            return False


# @parameterized_class([
#     {
#         "browser_class": browser_class,
#         "browser": browser,
#         "option": option,
#     }
#     for browser_class, browser, option in browsers
# ])


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
    current_time = None
    upper_bound_time = None

    @classmethod
    def setUpClass(cls):
        """
        Class method that is called before tests in an individual class are run.
        Initializes Selenium WebDriver and sets an implicit wait.
        """

        update_weather_fc.main()
        machine_learning_app.main()

        super().setUpClass()

        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_driver = Service(ChromeDriverManager().install())
        chrome = webdriver.Chrome(service=chrome_driver, options=chrome_options)

        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('-headless')
        firefox_driver = Service(GeckoDriverManager().install())
        firefox = webdriver.Firefox(service=firefox_driver, options=firefox_options)

        cls.selenium = chrome
        cls.selenium.implicitly_wait(5)
        cls.wait = WebDriverWait(cls.selenium, 5)
        cls.action = ActionChains(cls.selenium)
        cls.current_time = datetime.utcnow().astimezone(tz=tz.gettz('America/New_York'))
        cls.lower_exceeding_time = cls.current_time - timedelta(days=1)
        cls.upper_bound_time = cls.current_time + timedelta(days=15)
        cls.upper_exceeding_time = cls.upper_bound_time + timedelta(days=1)
        cls.hour_pattern = r"^(0?[0-9]|1[0-9]|2[0-3])$"
        cls.dt_selection = None

    @classmethod
    def tearDownClass(cls):
        """
        Class method that is called after all tests in an individual class have run.
        Quits the Selenium WebDriver.
        """

        cls.selenium.quit()
        super().tearDownClass()

    def _navigate_to_site(self):
        """
        Loads the page in Django's test environment.
        """

        self.selenium.get(f"{self.live_server_url}")

    def _open_nav_menu(self):
        """
        Opens the navigation/top menu. Requires the page to be loaded.
        """

        self.selenium.find_element(By.CSS_SELECTOR, 'button.btn.btn-dark.menu-button').click()
        return self.wait.until(
            ElementHasClass((By.XPATH, '//*[@id="offcanvasTop"]'), 'offcanvas offcanvas-top show'))

    def _close_nav_menu(self):
        """
        Closes the navigation/top menu. Requires the menu to be visible.
        """

        self.wait.until(EC.element_to_be_clickable(
            self.selenium.find_element(By.CSS_SELECTOR, 'button.btn-close'))).click()
        return self.wait.until(
            ElementHasClass((By.XPATH, '//*[@id="offcanvasTop"]'), 'offcanvas offcanvas-top'))

    def _open_search_menu(self):
        """
        Opens the search/bottom menu. Requires the page to be loaded.
        """

        self.selenium.find_element(By.CSS_SELECTOR, '.offcanvas-button').click()
        return self.wait.until(
            ElementHasClass((By.XPATH, '//*[@id="offcanvasBottom"]'), 'offcanvas offcanvas-bottom show'))

    def _close_search_menu(self):
        """
        Closes the search/bottom menu.
        """

        # calculate point in top 20% of window - needed to make bottom menu disappear
        window_size = self.selenium.get_window_size()
        x_coordinate = window_size["width"] / 2
        y_coordinate = window_size["height"] / 5

        self.action.reset_actions()

        # click on previously defined point to close bottom offcanvas menu and wait for it to disappear
        self.action.move_by_offset(x_coordinate, y_coordinate).click().perform()
        return self.wait.until(
            ElementHasClass((By.XPATH, '//*[@id="offcanvasBottom"]'), 'offcanvas offcanvas-bottom'))

    def _click_dt_selection(self):
        """
        Clicks on the date/time selection element in the search menu. Requires menu to be visible.
        """

        self.dt_selection = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.form-control')))
        self.dt_selection.click()

    def _next_month(self):
        """
        Clicks on the next month button. Requires date/time selection element to be active/expanded.
        """

        next_month_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.rdtNext')))
        self.action.move_to_element(next_month_button).click().perform()

    def _prev_month(self):
        """
        Clicks on the previous month button. Requires date/time selection element to be active/expanded.
        """

        prev_month_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.rdtPrev')))
        self.action.move_to_element(prev_month_button).click().perform()

    def _switch_to_dt(self):
        switch_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.rdtSwitch')))
        self.action.move_to_element(switch_button).click().perform()

    def _click_on_date(self, day, month, year):
        """
        Clicks on a specific date within the application's date picker.

        Args:
            day (int): The day of the month to select. Expected values are 1-31.
            month (int): The month to select. Expected values are 1-12, where 1
                represents January and 12 represents December.
            year (int): The year to select. This should be a valid four-digit year.
        """

        element = self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                              f'//td[@data-value="{day}" and @data-month="{month - 1}" and @data-year="{year}"]')))
        element.click()

    def _click_time_selection(self):
        """
        Clicks on the time selection button to open the selection. Requires date/time selection element to be active/expanded.
        """

        time_selection = self.selenium.find_element(By.CSS_SELECTOR, '.rdtTimeToggle')
        time_selection.click()

    def _next_hour(self):
        """
        Clicks on the next hour button. Requires time selection element to be active/expanded.
        """

        next_hour_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.rdtBtn')))
        self.action.move_to_element(next_hour_button).click().perform()

    def _prev_hour(self):
        """
        Clicks on the previous hour button. Requires time selection element to be active/expanded.
        """

        prev_hour_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.rdtBtn:nth-child(3)')))
        self.action.move_to_element(prev_hour_button).click().perform()

    def test_nav_menu_opens(self):
        self._navigate_to_site()
        self.assertTrue(self._open_nav_menu())

    def test_nav_menu_closes(self):
        self._navigate_to_site()
        self._open_nav_menu()
        self.assertTrue(self._close_nav_menu())

    def test_search_menu_opens(self):
        self._navigate_to_site()
        self.assertTrue(self._open_search_menu())

    def test_search_menu_closes(self):
        self._navigate_to_site()
        self._open_search_menu()
        self.assertTrue(self._close_search_menu())

    def test_lower_bound(self):
        self._navigate_to_site()
        self._open_search_menu()

        if self.lower_exceeding_time.month < self.current_time.month or self.lower_exceeding_time.year < self.current_time.year:
            self._click_dt_selection()
            self._prev_month()

        assert ElementHasClass((By.XPATH,
                                f'//td[@data-value="{self.lower_exceeding_time.day}" and @data-month="{self.lower_exceeding_time.month - 1}" and @data-year="{self.lower_exceeding_time.year}"]'),
                               'rdtDay rdtDisabled')(self.selenium)

    def test_upper_bound(self):
        self._navigate_to_site()
        self._open_search_menu()

        # navigate to the month with the last day that can be selected
        if self.upper_bound_time.month > self.current_time.month or self.upper_bound_time.year > self.current_time.year:
            self._click_dt_selection()
            self._next_month()
            # if the first day that can't be selected is in the month after the last selectable day, go to that month
            if self.upper_exceeding_time.month > self.upper_bound_time.month or self.upper_exceeding_time.year > self.upper_bound_time.year:
                self._next_month()

        assert ElementHasClass((By.XPATH,
                                f'//td[@data-value="{self.upper_exceeding_time.day}" and @data-month="{self.upper_exceeding_time.month - 1}" and @data-year="{self.upper_exceeding_time.year}"]'),
                               'rdtDay rdtDisabled')(self.selenium)

    def test_hour_rollover_upwards(self):
        self._navigate_to_site()
        self._open_search_menu()
        self._click_dt_selection()
        self._click_time_selection()

        time_value = ""
        click_counter = 0

        # check if hour rolls over correctly from 23 to 0
        while time_value != "0" and click_counter < 24:
            self._next_hour()
            time_value = self.wait.until(TextMatchesPattern((By.CSS_SELECTOR, '.rdtCount'), self.hour_pattern)).text
            click_counter += 1
        # assert the datetime value is equivalent to today's date at hour 0 and minute 0
        assert self.dt_selection.get_attribute("value") == self.current_time.replace(hour=0, minute=0).strftime(
            '%d/%m/%Y %H:%M')

    def test_hour_rollover_downwards(self):
        self._navigate_to_site()
        self._open_search_menu()
        self._click_dt_selection()
        self._click_time_selection()

        time_value = ""
        click_counter = 0

        # check if hour rolls over correctly from 0 to 23
        while time_value != "23" and click_counter < 24:
            self._prev_hour()
            time_value = self.wait.until(TextMatchesPattern((By.CSS_SELECTOR, '.rdtCount'), self.hour_pattern)).text
            click_counter += 1
        # assert the datetime value is equivalent to today's date at hour 23 and minute 0
        assert self.dt_selection.get_attribute("value") == self.current_time.replace(hour=23, minute=0).strftime(
            '%d/%m/%Y %H:%M')

    def test_last_day(self):
        self._navigate_to_site()
        self._open_search_menu()
        self._click_dt_selection()

        # navigate to the month with the last day that can be selected
        if self.upper_bound_time.month > self.current_time.month or self.upper_bound_time.year > self.current_time.year:
            self._next_month()
            # click on the last day
            self._click_on_date(self.upper_bound_time.day, self.upper_bound_time.month, self.upper_bound_time.year)

    def test_search(self):
        self._navigate_to_site()
        self._open_search_menu()

        # select tree level - change second to last div:nth-child -> div:nth-child(tree level)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                    '.button-container > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > input:nth-child(1)'))).click()

        # select busyness level - change second to last div:nth-child -> div:nth-child(busyness level)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                    '.button-container > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > input:nth-child(1)'))).click()

        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn:nth-child(5)'))).click()

        scroll_container = self.selenium.find_element(By.CSS_SELECTOR, '.scroll-container')

        # Find the inner element that you want to scroll to
        result = scroll_container.find_element(By.CSS_SELECTOR,
                                               'div.carousel-item:nth-child(1) > div:nth-child(1) > div:nth-child(1)')

        # scroll the container to the bottom so the results are visible
        self.selenium.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)

        result_patterns = {'rank': r'^\d+.$', 'zone': r'^([\w/-]+\s*)+$', 'buildings': r'^([\w/-]+\s*)+\sbuildings$',
                           'busyness': r'^BUSYNESS \d$', 'trees': r'^TREES \d$'}

        for i in range(1, 11):
            rank = self.selenium.find_element(By.CSS_SELECTOR,
                                              f'div.carousel-item:nth-child({i}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1)')
            zone = self.selenium.find_element(By.CSS_SELECTOR,
                                              f'div.carousel-item:nth-child({i}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > p:nth-child(2)')
            buildings = self.selenium.find_element(By.CSS_SELECTOR,
                                                   f'div.carousel-item:nth-child({i}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > p:nth-child(3)')
            busyness = self.selenium.find_element(By.CSS_SELECTOR,
                                                  f'div.carousel-item:nth-child({i}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > p:nth-child(1)')
            trees = self.selenium.find_element(By.CSS_SELECTOR,
                                               f'div.carousel-item:nth-child({i}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > p:nth-child(2)')

            result_values = {'rank': rank.text, 'zone': zone.text, 'buildings': buildings.text,
                             'busyness': busyness.text, 'trees': trees.text}

            for j in result_values.keys():
                self.assertTrue(bool(re.match(result_patterns.get(j), result_values.get(j))),
                                f'In result {i}: {result_values.get(j)} is not an expected pattern for {j}')

            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.carousel-control-next-icon'))).click()
            time.sleep(1)
