from typing import List
from selenium.common import NoSuchElementException
from selenium.webdriver.support.select import Select

from helper_functions.logging import log_info
from pages.base_page import BasePage
from resources.locators import CommonLocator
from resources.selenium_data import SeleniumData


class DropDownPage(BasePage):
    """Page Object for DropDownPage functionality."""
    def __init__(self, driver):
        super().__init__(driver)
        self.load_page(SeleniumData.base_url)

    @property
    def drop_down(self)-> Select:
        """Initialize dropdown element."""
        log_info("Initialising Dropdown elements.")
        return Select(self.driver.find_element(*CommonLocator.dropdown_select))

    def get_all_selected_options(self)-> List[str]:
        """Function returns a list of all selected dropdown options assuming
        multiple selections is enabled."""
        log_info("Get list of all selected drop down options.")
        selected_options = [
            option.text
            for option in self.drop_down.options
            if option.get_attribute("selected")
        ]
        return selected_options

    def select_option(self, option:str)-> None:
        """Select drop down option."""
        log_info(f"Selecting : {option}")
        try:
              self.drop_down.select_by_visible_text(option)
        except NoSuchElementException as error:
            raise f"Option not available: {error}"

    def is_option_selected(self, option:str)-> bool:
        """Verify Dropdown option is selected"""
        log_info("Verify drop down option is selected.")
        return option in self.drop_down.first_selected_option.text
