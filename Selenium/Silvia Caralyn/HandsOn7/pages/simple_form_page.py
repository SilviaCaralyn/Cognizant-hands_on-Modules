"""
HANDS-ON 7 - Task 1: SimpleFormPage — encapsulates the Simple Form Demo page.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SimpleFormPage(BasePage):
    # Locators as class-level tuples — never hardcode inline in methods
    MESSAGE_INPUT = (By.ID, "user-message")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "input[onclick='showInput()']")
    DISPLAYED_MESSAGE = (By.ID, "message")

    def enter_message(self, text):
        field = self.wait_for_element(self.MESSAGE_INPUT)
        field.clear()
        field.send_keys(text)

    def click_submit(self):
        self.wait_for_clickable(self.SUBMIT_BUTTON).click()

    def get_displayed_message(self):
        return self.wait_for_element(self.DISPLAYED_MESSAGE).text
