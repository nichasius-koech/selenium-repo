from typing import List
from selenium.webdriver.remote.webelement import WebElement

from helper_functions.logging import log_info
from pages.base_page import BasePage
from resources.locators import WebTableLocator
from resources.selenium_data import SeleniumData


class WebTable(BasePage):
    """Page Object for WebTable functionality."""

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.load_page(SeleniumData.web_table_url)

    @property
    def table(self) -> WebElement:
        """Returns table web element."""
        return self.driver.find_element(*WebTableLocator.table)

    def get_table_headers(self) -> List[str]:
        """Return table headers."""
        log_info("Retrieving Table Headers.")
        table_headers: List[str] = [
            th.text.strip() for th in self.table.find_elements(*WebTableLocator.table_headers)]
        return table_headers

    def get_table_rows(self) -> List[dict]:
        """Return table rows values mapped to table headers-."""
        log_info("Retrieving Table Rows.")
        headers = self.get_table_headers()
        rows=self.table.find_elements(*WebTableLocator.table_rows)
        table_rows=[]
        for row in rows:
            cells = row.find_elements(*WebTableLocator.row_cells)
            row_values = [cell.text.strip() for cell in cells]
            if not row_values:
                # Skip empty rows
                continue
            table_rows.append(dict(zip(headers, row_values)))
        return table_rows

    def add_table_record(self):
        # self.wait_clickable(edit_btns[2]).click()
        ...