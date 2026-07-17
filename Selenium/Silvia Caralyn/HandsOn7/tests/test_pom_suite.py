"""
HANDS-ON 7 - Task 2: Fully refactored POM test suite.
Zero driver.find_element calls appear in this file — all interactions
go through Page Object methods.

Run from the automation_scripts/ folder:
    pytest tests/ -v --html=report.html --self-contained-html
"""

import sys
import os

# Allow `pages` package to be importable when running from automation_scripts/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.simple_form_page import SimpleFormPage
from pages.checkbox_page import CheckboxPage
from pages.dropdown_page import DropdownPage
from pages.input_form_page import InputFormPage


def test_simple_form_submission(driver, base_url):
    page = SimpleFormPage(driver)
    page.navigate_to(base_url + "simple-form-demo/")
    page.enter_message("Hello Selenium")
    page.click_submit()
    assert page.get_displayed_message() == "Hello Selenium"


def test_checkbox_demo(driver, base_url):
    page = CheckboxPage(driver)
    page.navigate_to(base_url + "checkbox-demo/")
    page.check_option(0)
    assert page.is_option_checked(0) is True
    page.uncheck_option(0)
    assert page.is_option_checked(0) is False


def test_dropdown_selection(driver, base_url):
    page = DropdownPage(driver)
    page.navigate_to(base_url + "select-dropdown-demo/")
    page.select_day("Wednesday")
    assert page.get_selected_day() == "Wednesday"


def test_input_form_submit(driver, base_url):
    page = InputFormPage(driver)
    page.navigate_to(base_url + "input-form-demo/")
    page.fill_form(
        name="Jane Doe",
        email="jane.doe@example.com",
        phone="9876543210",
        address="221B Baker Street",
    )
    page.submit_form()
    assert "success" in page.get_success_message().lower()


# Step 59: Maintenance comment
# If the Submit button's ID changed from 'submit' to 'btn-submit' in a FLAT
# (non-POM) script, every single test file that has a hardcoded
# `driver.find_element(By.ID, 'submit')` call would break, and a developer
# would need to find-and-replace that locator across every affected test
# file individually — easy to miss one and leave a silently broken test.
#
# With POM, the locator exists in exactly ONE place: the SUBMIT_BUTTON
# tuple inside the relevant Page class (e.g. SimpleFormPage.SUBMIT_BUTTON).
# Updating that single class-level constant fixes every test that uses
# page.click_submit(), because none of the test files reference the
# locator directly. This is the core maintainability benefit of POM.
