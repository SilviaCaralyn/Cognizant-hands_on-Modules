"""
HANDS-ON 6: pytest test suite for the LambdaTest Selenium Playground.
Run with: pytest test_playground.py -v --html=report.html --self-contained-html
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


# Step 45: parameterised form submission test — 3 separate runs
@pytest.mark.parametrize("message", ["Hello", "Selenium Automation", "12345"])
def test_simple_form_submission(driver, base_url, message):
    driver.get(base_url + "simple-form-demo/")
    driver.find_element(By.ID, "user-message").send_keys(message)
    driver.find_element(By.CSS_SELECTOR, "input[onclick='showInput()']").click()

    displayed = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "message"))
    )
    assert displayed.text == message


def test_checkbox_demo(driver, base_url):
    driver.get(base_url + "checkbox-demo/")
    checkbox = driver.find_element(By.ID, "isAgeSelected")

    checkbox.click()
    assert checkbox.is_selected() is True

    checkbox.click()
    assert checkbox.is_selected() is False


def test_dropdown_selection(driver, base_url):
    driver.get(base_url + "select-dropdown-demo/")
    dropdown_el = driver.find_element(By.ID, "select-demo")
    select = Select(dropdown_el)

    select.select_by_visible_text("Wednesday")

    assert select.first_selected_option.text == "Wednesday"
