"""
HANDS-ON 7 - Task 1: CheckboxPage — encapsulates the Checkbox Demo page.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckboxPage(BasePage):
    CHECKBOXES = (By.CSS_SELECTOR, "#colorbox li input[type='checkbox']")

    def _get_checkbox(self, index):
        checkboxes = self.driver.find_elements(*self.CHECKBOXES)
        return checkboxes[index]

    def check_option(self, index):
        box = self._get_checkbox(index)
        if not box.is_selected():
            box.click()

    def uncheck_option(self, index):
        box = self._get_checkbox(index)
        if box.is_selected():
            box.click()

    def is_option_checked(self, index):
        return self._get_checkbox(index).is_selected()
