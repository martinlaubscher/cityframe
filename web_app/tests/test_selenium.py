import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
web_app_path = os.path.dirname(current_path)
sys.path.append(web_app_path)

import time
import datetime
import re
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from dateutil import tz
from datetime import datetime, timedelta
from parameterized import parameterized_class
from django.db import connections
from django.test import tag
from tests.setup.common_setup import CommonSetup


class ElementHasValue:
    """
    A callable class to check whether an HTML element has a non-empty value attribute.

    Attributes:
        locator (tuple): A tuple containing the strategy to locate the element and the value to search for.

    Methods:
        __call__(driver): Returns True if the element's value attribute is not empty, False otherwise.
    """

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        return element.get_attribute("value") != ""


class ElementHasClass(object):
    """
    A callable class to check whether an HTML element has a specific CSS class.

    Attributes:
        locator (tuple): A tuple containing the strategy to locate the element and the value to search for.
        css_class (str): The CSS class to look for in the element's class attribute.

    Methods:
        __call__(driver): Returns True if the element's class attribute matches the given CSS class, False otherwise.
    """

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
    """
    A callable class to check whether the text of an HTML element matches a given pattern.

    This class is used to verify if the text content of a specific HTML element identified by a locator
    matches a given regular expression pattern.

    Attributes:
        locator (tuple): A tuple containing the strategy to locate the element and the value to search for.
        pattern (str): The regular expression pattern to match against the element's text.

    Methods:
        __call__(driver): Returns the element if the text matches the pattern, False otherwise.
    """

    def __init__(self, locator, pattern):
        self.locator = locator
        self.pattern = pattern

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if bool(re.match(self.pattern, element.text)):
            return element
        else:
            return False


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_driver = Service(ChromeDriverManager().install())
chrome = webdriver.Chrome(service=chrome_driver, options=chrome_options)

firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('-headless')
firefox_driver = Service(GeckoDriverManager().install())
firefox = webdriver.Firefox(service=firefox_driver, options=firefox_options)


@parameterized_class([
    {"browser": chrome},
    {"browser": firefox},
])
class IntegrationTests(StaticLiveServerTestCase, CommonSetup):
    """
    IntegrationTests class to test the front-end of a web application.

    This class utilizes Selenium WebDriver to perform automated integration tests
    on the application's UI. It includes tests for navigation menus, date and time
    selection, rollover of hours, lower and upper bound selection, and specific
    functional tests such as searching.

    Attributes:
        selenium (webdriver): The Selenium WebDriver instance used for browser automation.
        current_time (datetime): The current time in a specific timezone.
        upper_bound_time (datetime): The upper bound time for date/time selection.
        lower_exceeding_time (datetime): The lower exceeding time for date/time selection.
        upper_exceeding_time (datetime): The upper exceeding time for date/time selection.
        hour_pattern (str): A regular expression pattern for validating hour format.
        dt_selection (WebElement): A WebElement representing the date/time selection element.
        wait (WebDriverWait): WebDriverWait instance to apply explicit waits.
        action (ActionChains): ActionChains instance to perform complex actions.

    Class Methods:
        setUpClass(): Initializes WebDriver and sets up the testing environment.
        tearDownClass(): Quits the Selenium WebDriver.
        _navigate_to_site(): Navigates to the testing site.
        _open_nav_menu(): Opens the navigation/top menu.
        _close_nav_menu(): Closes the navigation/top menu.
        _open_search_menu(): Opens the search/bottom menu.
        _close_search_menu(): Closes the search/bottom menu.
        _click_dt_selection(): Clicks on the date/time selection element in the search menu.
        _next_month(): Clicks on the next month button in the date picker.
        _prev_month(): Clicks on the previous month button in the date picker.
        _switch_to_dt(): Switches to the date/time picker.
        _click_on_date(day, month, year): Clicks on a specific date within the application's date picker.
        _click_time_selection(): Clicks on the time selection button to open the selection.
        _next_hour(): Clicks on the next hour button in the time picker.
        _prev_hour(): Clicks on the previous hour button in the time picker.

    Test Methods:
        test_nav_menu_opens(): Tests if the navigation menu opens successfully.
        test_nav_menu_closes(): Tests if the navigation menu closes successfully.
        test_search_menu_opens(): Tests if the search menu opens successfully.
        test_search_menu_closes(): Tests if the search menu closes successfully.
        test_lower_bound(): Tests date selector lower bound.
        test_upper_bound(): Tests date selector upper bound.
        test_hour_rollover_upwards(): Tests hour rollover from 23 to 0.
        test_hour_rollover_downwards(): Tests hour rollover from 0 to 23.
        test_last_day(): Tests last day selection.
        test_search(): Tests search feature functionality.
    """

    selenium = None
    current_time = None
    upper_bound_time = None
    browser = None

    @classmethod
    def setUpClass(cls):
        """
        Class method that is called before tests in an individual class are run.
        Initializes Selenium WebDriver and sets an implicit wait.
        """

        super().setUpClass()

        # check if schema 'cityframe' already exists
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'cityframe';")
            schema_exists = cursor.fetchone()

        # only run common_setup if the schema does not exist
        if not schema_exists:
            cls.common_setup()

        cls.selenium = cls.browser
        cls.selenium.implicitly_wait(5)
        cls.wait = WebDriverWait(cls.selenium, 5)
        cls.action = ActionChains(cls.selenium)
        cls.current_time = datetime.utcnow().replace(tzinfo=tz.UTC).astimezone(tz=tz.gettz('America/New_York'))
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

        self.selenium.find_element(By.CSS_SELECTOR, '#SVGRepo_iconCarrier > path:nth-child(1)').click()
        return self.wait.until(
            ElementHasClass((By.XPATH, '//*[@id="offcanvasTop"]'), 'offcanvas offcanvas-top show'))

    def _close_nav_menu(self):
        """
        Closes the navigation/top menu. Requires the menu to be visible.
        """

        # calculate point at bottom of window - needed to make nav menu disappear
        window_size = self.selenium.get_window_size()
        x_coordinate = window_size["width"] / 2
        y_coordinate = window_size["height"] - (window_size["height"] / 5)

        self.action.reset_actions()

        # click on previously defined point to close bottom offcanvas menu and wait for it to disappear
        self.action.move_by_offset(x_coordinate, y_coordinate).click().perform()
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
        """
        Switches to the datetime selection mode in the UI.
        """

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

    def _select_style(self, style):
        """
        Selects a specific architecture style option from the dropdown menu

        Args:
            style (int): The style to be selected as an integer representing the index of the option.
        """

        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#style-selection > select:nth-child(1)'))).click()
        self.selenium.find_element(By.CSS_SELECTOR,
                                   f'#style-selection > select:nth-child(1) > option:nth-child({style})').click()

    def _select_zone_type(self, zone_type):
        """
        Selects a specific zone type option from the dropdown menu

        Args:
            zone_type (int): The zone type to be selected as an integer representing the index of the option.
        """

        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#type-selection > select:nth-child(1)'))).click()
        self.selenium.find_element(By.CSS_SELECTOR,
                                   f'#type-selection > select:nth-child(1) > option:nth-child({zone_type})').click()

    def _select_weather(self, weather):
        """
        Selects a specific weather option from the dropdown menu

        Args:
            weather (int): The weather to be selected as an integer representing the index of the option.
        """

        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.weather-select'))).click()
        self.selenium.find_element(By.CSS_SELECTOR, f'.weather-select > option:nth-child({weather})').click()

    def _get_selections(self, level):
        """
        Gets the selected values from the search menu. For the radio buttons, returns whether the button with the selected level is checked.

        Args:
            level (int): The radio button level (both trees and busyness).

        Returns:
            dict: A dictionary with the values for each of the selections.
        """

        busyness_selection = self.selenium.find_element(By.CSS_SELECTOR,
                                                        f'#busyness-selection > div:nth-child({level}) > input:nth-child(1)').get_attribute(
            'checked')
        tree_selection = self.selenium.find_element(By.CSS_SELECTOR,
                                                    f'#tree-selection > div:nth-child({level}) > input:nth-child(1)').get_attribute(
            'checked')
        style_selection = Select(self.selenium.find_element(By.CSS_SELECTOR,
                                                            '#style-selection > select:nth-child(1)')).first_selected_option.text
        zone_type_selection = Select(self.selenium.find_element(By.CSS_SELECTOR,
                                                                '#type-selection > select:nth-child(1)')).first_selected_option.text
        weather_selection = Select(
            self.selenium.find_element(By.CSS_SELECTOR, '.weather-select')).first_selected_option.text

        return {'busyness': busyness_selection, 'trees': tree_selection, 'style': style_selection,
                'zone_type': zone_type_selection, 'weather': weather_selection}

    @tag('open_nav')
    def test_nav_menu_opens(self):
        """
        Tests if the navigation menu opens successfully.
        """

        self._navigate_to_site()
        self.assertTrue(self._open_nav_menu())

    @tag('close_nav')
    def test_nav_menu_closes(self):
        """
        Tests if the navigation menu closes successfully.
        """

        self._navigate_to_site()
        self._open_nav_menu()
        self.assertTrue(self._close_nav_menu())

    @tag('open_search')
    def test_search_menu_opens(self):
        """
        Tests if the search menu opens successfully.
        """

        self._navigate_to_site()
        self.assertTrue(self._open_search_menu())

    @tag('close_search')
    def test_search_menu_closes(self):
        """
        Tests if the search menu closes successfully.
        """

        self._navigate_to_site()
        self._open_search_menu()
        self.assertTrue(self._close_search_menu())

    @tag('date_lower')
    def test_lower_bound(self):
        """
        Tests if the date selector correctly disables dates below a certain bound.
        """

        self._navigate_to_site()
        self._open_search_menu()

        if self.lower_exceeding_time.month < self.current_time.month or self.lower_exceeding_time.year < self.current_time.year:
            self._click_dt_selection()
            self._prev_month()

        self.assertTrue(ElementHasClass((By.XPATH,
                                         f'//td[@data-value="{self.lower_exceeding_time.day}" and @data-month="{self.lower_exceeding_time.month - 1}" and @data-year="{self.lower_exceeding_time.year}"]'),
                                        'rdtDay rdtDisabled')(self.selenium))

    @tag('date_upper')
    def test_upper_bound(self):
        """
        Tests if the date selector correctly disables dates above a certain bound.
        """

        self._navigate_to_site()
        self._open_search_menu()

        # navigate to the month with the last day that can be selected
        if self.upper_bound_time.month > self.current_time.month or self.upper_bound_time.year > self.current_time.year:
            self._click_dt_selection()
            self._next_month()
            # if the first day that can't be selected is in the month after the last selectable day, go to that month
            if self.upper_exceeding_time.month > self.upper_bound_time.month or self.upper_exceeding_time.year > self.upper_bound_time.year:
                self._next_month()

        self.assertTrue(ElementHasClass((By.XPATH,
                                         f'//td[@data-value="{self.upper_exceeding_time.day}" and @data-month="{self.upper_exceeding_time.month - 1}" and @data-year="{self.upper_exceeding_time.year}"]'),
                                        'rdtDay rdtDisabled')(self.selenium))

    @tag('hour_up')
    def test_hour_rollover_upwards(self):
        """
        Tests if the hour selector rolls over correctly from 23 to 0.
        """

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
        self.assertEqual(self.dt_selection.get_attribute("value"), self.current_time.replace(hour=0, minute=0).strftime(
            '%d/%m/%Y %H:%M'))

    @tag('hour_down')
    def test_hour_rollover_downwards(self):
        """
        Tests if the hour selector rolls over correctly from 0 to 23.
        """

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
        self.assertEqual(self.dt_selection.get_attribute("value"),
                         self.current_time.replace(hour=23, minute=0).strftime(
                             '%d/%m/%Y %H:%M'))

    @tag('last')
    def test_last_day(self):
        """
        Tests if the date selector can correctly select the last allowable day.
        """

        self._navigate_to_site()
        self._open_search_menu()
        self._click_dt_selection()

        # navigate to the month with the last day that can be selected
        if self.upper_bound_time.month > self.current_time.month or self.upper_bound_time.year > self.current_time.year:
            self._next_month()
        # click on the last day
        self._click_on_date(self.upper_bound_time.day, self.upper_bound_time.month, self.upper_bound_time.year)

        self.assertEqual(self.dt_selection.get_attribute("value"),
                         self.upper_bound_time.replace(hour=self.current_time.hour, minute=0).strftime(
                             '%d/%m/%Y %H:%M'))

    @tag('search')
    def test_search(self):
        """
        Tests the functionality of the search feature including style, tree level, and busyness level selection.
        """

        style_dict = {
            1: 'neo-Georgian',
            2: 'Greek Revival',
            3: 'Romanesque Revival',
            4: 'neo-Grec',
            5: 'Renaissance Revival',
            6: 'Beaux-Arts',
            7: 'Queen Anne',
            8: 'Italianate',
            9: 'Federal',
            10: 'neo-Renaissance'
        }

        self._navigate_to_site()
        self._open_search_menu()

        for i in range(0, 10):

            tree_levels = (5, 4, 3, 2, 1, 2, 4, 5, 1, 3)
            busyness_levels = (1, 2, 3, 4, 5, 1, 2, 3, 4, 5)
            zone_types = (1, 2, 3, 4, 1, 2, 3, 4, 2, 3)
            weather_options = (1, 2, 3, 8, 1, 2, 3, 8, 2, 3)

            # select tree level - change second to last div:nth-child -> div:nth-child(tree level)
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                        f'.button-container > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child({tree_levels[i]}) > input:nth-child(1)'))).click()

            # select busyness level - change second to last div:nth-child -> div:nth-child(busyness level)
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                        f'.button-container > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child({busyness_levels[i]}) > input:nth-child(1)'))).click()

            # select the style (by its int value)
            self._select_style(i + 1)

            self._select_zone_type(zone_types[i])

            self._select_weather(weather_options[i])

            # click the search button
            self.wait.until(EC.element_to_be_clickable((By.ID, 'search-button'))).click()

            # scroll the container to the bottom so the results are visible
            scroll_container = self.selenium.find_element(By.CSS_SELECTOR, '.scroll-container')
            self.selenium.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)

            # wait one second to make sure results have had time to load
            time.sleep(1)

            result_patterns = {'rank': r'^\d+$',
                               'zone': r'^([\w/\'-]+\s*)+$',
                               'buildings': rf'^\d+\sbuilding[s]*$',
                               'busyness': r'^level:\s\d$',
                               'trees': r'^level:\s\d$',
                               'zone_type': r'^\d+%\s\w+$'}

            # go through all the results in the carousel
            for j in range(0, 10):
                rank = self.selenium.find_element(By.XPATH,
                                                  "//*[@class='rank'][ancestor::*[@class='carousel-item active']]")
                zone = self.selenium.find_element(By.XPATH,
                                                  "//*[@class='zone'][ancestor::*[@class='carousel-item active']]")
                busyness = self.selenium.find_elements(By.XPATH,
                                                       "//*[@class='level'][ancestor::*[@class='carousel-item active']]")[
                    0]
                trees = self.selenium.find_elements(By.XPATH,
                                                    "//*[@class='level'][ancestor::*[@class='carousel-item active']]")[
                    1]
                buildings = self.selenium.find_element(By.XPATH,
                                                       "//*[@class='building-counting'][ancestor::*[@class='carousel-item active']]")
                zone_type = self.selenium.find_element(By.XPATH,
                                                       "//*[@class='type-percent'][ancestor::*[@class='carousel-item active']]")

                result_values = {'rank': rank.text, 'zone': zone.text, 'buildings': buildings.text,
                                 'busyness': busyness.text, 'trees': trees.text, 'zone_type': zone_type.text}

                # assert that the result values match the expected patterns
                for key in result_values.keys():
                    self.assertTrue(bool(re.match(result_patterns.get(key), result_values.get(key))),
                                    f'In result {j + 1}: {result_values.get(key)} is not an expected pattern for {key}')

                # click on the next result button
                self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.carousel-control-next-icon'))).click()
                # wait for the carousel to transition to the next result
                time.sleep(1)

    @tag('failed_search')
    def test_failed_search(self):
        """
        Tests that a search with no results is handled correctly. Assumes it's not snowing in the next 16 days.
        """

        self._navigate_to_site()
        self._open_search_menu()

        self._select_weather(10)

        # click the search button
        self.wait.until(EC.element_to_be_clickable((By.ID, 'search-button'))).click()

        # scroll the container to the bottom so the results are visible
        scroll_container = self.selenium.find_element(By.CSS_SELECTOR, '.scroll-container')
        self.selenium.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)

        error_msg = self.selenium.find_element(By.CSS_SELECTOR, 'span.error-alert:nth-child(1)')

        self.assertEqual(error_msg.text, 'Nothing here!')

    @tag('clear_search')
    def test_clear_search(self):
        """
        Tests that the clear search button resets the values as expected.
        """

        self._navigate_to_site()
        self._open_search_menu()

        # make some selections
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                    f'.button-container > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child({3}) > input:nth-child(1)'))).click()
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                    f'.button-container > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child({3}) > input:nth-child(1)'))).click()
        self._select_style(7)
        self._select_zone_type(3)
        self._select_weather(3)

        # get the selected values
        selections = self._get_selections(3)
        checks = {'busyness': 'true', 'trees': 'true', 'style': 'Queen Anne', 'zone_type': 'Park', 'weather': 'Clouds'}
        # check the selected values have been stored
        for key in selections.keys():
            self.assertEqual(selections.get(key), checks.get(key))

        # click the clear search button
        self.wait.until(EC.element_to_be_clickable((By.ID, 'clear-search-button'))).click()

        # get the selected values
        selections = self._get_selections(1)
        checks = {'busyness': 'true', 'trees': 'true', 'style': 'neo-Georgian', 'zone_type': 'Commercial',
                  'weather': 'All'}
        # check the values have been reset
        for key in selections.keys():
            self.assertEqual(selections.get(key), checks.get(key))
