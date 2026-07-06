import random
from pytest import fixture
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

from pages.slider import Slider
from pages.web_table import WebTable
from pages.login import LoginPage
from pages.dropdown import DropDownPage
from pages.date_picker import DatePicker
from pages.file_upload import FileUpload
from resources.selenium_data import SeleniumData


def pytest_addoption(parser):
    parser.addoption(
        "--on-browser",
        action="store",
        default="chrome",
        help="Browser to run tests against"
    )

def get_driver(browser) -> WebDriver:
    """
    This fixture initializes a WebDriver for the specified browser,
     and ensures proper cleanup after the test execution by quitting the driver.
    """
    if browser.lower() == "chrome":
        options = Options()
        # Important options for CI
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=options)
    elif browser.lower() == "firefox":
        driver = webdriver.Firefox()
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    return driver

@fixture
def browser(request) -> str:
    """Get terminal option for which browser to use."""
    return request.config.getoption("--on-browser")

@fixture
def driver(browser):
    driver = get_driver(browser)
    yield driver
    driver.quit()

@fixture
def slider(driver: WebDriver) -> Slider:
    """Instantiate Slider class."""
    return Slider(driver)

@fixture
def drop_down(driver: WebDriver) -> DropDownPage:
    """Instantiate DropDownPage class."""
    return DropDownPage(driver)

@fixture
def file_upload(driver: WebDriver) -> FileUpload:
    """Instantiate FileUpload class."""
    return FileUpload(driver)

@fixture
def date_picker(driver: WebDriver) -> DatePicker:
    """Instantiate DatePicker class."""
    return DatePicker(driver)

@fixture
def web_table(driver: WebDriver) -> WebTable:
    """Instantiate WebTable class."""
    return WebTable(driver)

import pytest
from selenium.webdriver.remote.webdriver import WebDriver


@pytest.fixture
def login(driver: WebDriver):
    """Login helper fixture."""
    login_page = LoginPage(driver)

    def _login(username: str, password: str):
        login_page.enter_user_name(username)
        login_page.enter_password(password)
        login_page.tap_login_btn()
        return login_page

    return _login


@fixture(params=SeleniumData.calendar_months, ids=lambda c: c)
def months(request) -> str:
    """Fixture returns Calendar months one at a time.'"""
    return request.param

@fixture()
def all_calendar_months() -> str:
    """Fixture returns Calendar months.'"""
    return SeleniumData.calendar_months

@fixture
def random_months(all_calendar_months :str) -> list[str]:
    """Fixture returns 5 Calendar months one at a time.'"""
    random_months = 5
    return random.sample(all_calendar_months, random_months)
