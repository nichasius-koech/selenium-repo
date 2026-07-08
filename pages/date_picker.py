from datetime import datetime
from typing import List
from selenium.common import StaleElementReferenceException, TimeoutException
from selenium.webdriver.remote.webelement import WebElement

from helper_functions.logging import log_info, log_debug
from pages.base_page import BasePage
from resources.locators import CommonLocator
from resources.selenium_data import SeleniumData


class DatePicker(BasePage):
    """Page Object for DatePicker functionality."""

    def __init__(self, driver):
        super().__init__(driver)
        self.load_page(SeleniumData.base_url)

    @property
    def month_switch(self) -> WebElement:
        """Returns the month switch element"""
        return self.driver.find_element(*CommonLocator.month_switch)

    @property
    def next_month(self) -> WebElement:
        """Returns the next element"""
        return self.driver.find_element(*CommonLocator.next_month)

    @property
    def prev_month(self):
        """Returns the prev element"""
        return self.driver.find_element(*CommonLocator.prev_month)

    @property
    def date_input(self) -> WebElement:
        """Returns the Date Field element."""
        return self.wait_clickable(CommonLocator.date_input)

    def clear_existing_date(self) -> None:
        """"Clear date field."""
        log_info("Clear date field.")
        self.date_input.clear()

    def tap_date_field(self) -> None:
        """Tap Date input field."""
        log_debug("Tap Date input field.")
        self.date_input.click()

    def is_calendar_displayed(self) -> bool:
        """Return True if Calendar is displayed, else False."""
        is_calendar=self.is_element_visible(CommonLocator.month_switch)
        log_info(f"Is Calendar Displayed ? : {is_calendar}")
        return is_calendar

    def tap_month_switch(self)-> None:
        """Tap on Month switch menu"""
        log_info("Tap on Month switch menu")
        if not self.is_element_visible(CommonLocator.all_months):
            self.month_switch.click()

    def tap_next_icon(self)-> None:
        """Tap on Next icon."""
        log_info("Tap on Next icon.")
        self.next_month.click()

    def tap_prev_icon(self)-> None:
        """Tap on Prev icon."""
        log_info("Tap on Prev icon.")
        self.prev_month.click()

    def navigate_to_month(self, target_month: str) -> None:
        """Navigate to specified month via date picker switch."""
        log_info(f"Navigate to month: {target_month}.")
        for _ in range(len(SeleniumData.calendar_months)):
            if self.month_switch.text.startswith(target_month):
                return
            self.tap_next_icon()
        raise AssertionError(f"Month '{target_month}' not reached")

    def select_month(self, month_name: str) -> None:
        """Select specified month."""
        log_info(f"Select month: {month_name}.")
        self.tap_month_switch()
        month_locator = CommonLocator.month_by_name(month_name)
        try:
            self.wait_clickable(month_locator).click()
        except TimeoutException:
            raise AssertionError(f"Month '{month_name}' not found")

    def get_all_months(self)-> list[WebElement]:
        """Return a list of all months in Calendar."""
        log_info("Return a list of all months in Calendar.")
        self.tap_month_switch()
        return self.driver.find_elements(*CommonLocator.all_months)

    def get_dates(self) -> List[WebElement] :
        """Get available dates for a selected month."""
        log_info("Get available dates for a selected month.")
        return self.driver.find_elements(*CommonLocator.all_dates)

    def select_date(self, date_val: int) -> None:
        """Select a given calendar date. Hanles stale elements in case of refresh."""
        log_info(f"Select date: {date_val}")
        date = CommonLocator.date_by_value(date_val)
        for trial in range(3):
            try:
                self.wait_clickable(date).click()
                return
            except StaleElementReferenceException:
                if trial == 2:
                    raise

    def navigate_to_year(self, year):
        """Select a year."""
        ...

    def select_date_month_year(self, year: int, month: str, day: int) -> None:
        """Set date, month and year."""
        log_info(f"Select date: {day}, Month : {month}, Year: {year}.")
        self.navigate_to_year(year)
        self.select_month(month)
        self.select_date(day)

    def verify_date_set(self, date_set: int) -> bool:
        """Verify thet the selected date is set."""
        date_val = self.date_input.get_attribute("value")
        parsed = datetime.strptime(date_val, "%m/%d/%Y")
        log_debug(f"Is date: {date_set} selected ? : {parsed.day == date_set}")
        return parsed.day == date_set

    def verify_month_selected(self, month: str) -> bool:
        """Verify thet the selected month is set."""
        is_month = month in self.month_switch.text
        log_debug(f"Is selected month {month} selected ? : {is_month}")
        return is_month


