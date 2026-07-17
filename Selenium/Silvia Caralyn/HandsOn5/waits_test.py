"""
HANDS-ON 5 - Task 2: WebDriverWait and Expected Conditions
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait as FluentWebDriverWait
from selenium.common.exceptions import NoSuchElementException
from setup_test import build_driver, BASE_URL


def test_explicit_wait_for_alert():
    """Step 36: click a button, wait for alert visibility, assert text."""
    driver = build_driver(headless=False)
    try:
        driver.get(BASE_URL + "bootstrap-alerts/")
        driver.find_element(By.ID, "success-alert").click()

        alert_div = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        assert "successfully" in alert_div.text.lower()
        print("Alert text verified:", alert_div.text)
    finally:
        driver.quit()


def compare_sleep_vs_explicit_wait():
    """Step 37: time.sleep(3) vs explicit wait, compare durations."""
    # Version A: time.sleep(3)
    driver = build_driver(headless=False)
    try:
        driver.get(BASE_URL + "bootstrap-alerts/")
        start = time.time()
        driver.find_element(By.ID, "success-alert").click()
        time.sleep(3)  # BAD: always waits the full 3 seconds, even if alert
                        # appeared in 200ms, and fails outright if it takes 3.5s.
        alert_div = driver.find_element(By.CSS_SELECTOR, ".alert-success")
        print("sleep() version took:", round(time.time() - start, 2), "s | text:", alert_div.text)
    finally:
        driver.quit()

    # Version B: explicit wait
    driver = build_driver(headless=False)
    try:
        driver.get(BASE_URL + "bootstrap-alerts/")
        start = time.time()
        driver.find_element(By.ID, "success-alert").click()
        alert_div = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        print("Explicit wait version took:", round(time.time() - start, 2), "s | text:", alert_div.text)
        # On a fast machine this finishes as soon as the element appears
        # (often faster than the fixed 3s sleep). On a slow machine, it
        # keeps polling up to 10s instead of failing prematurely at 3s —
        # so it's both faster on average AND more reliable.
    finally:
        driver.quit()


def test_element_to_be_clickable():
    """Step 38: wait for clickability before clicking."""
    driver = build_driver(headless=False)
    try:
        driver.get(BASE_URL + "bootstrap-alerts/")
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "success-alert"))
        )
        button.click()
        # Difference:
        # - visibility_of_element_located: element exists in the DOM AND is
        #   displayed (not display:none / not zero-size). Does NOT guarantee
        #   it's interactable.
        # - element_to_be_clickable: everything visibility_of_element_located
        #   checks, PLUS the element is enabled (not disabled) and not
        #   obscured by another element on top of it — safe to click.
        print("Clicked button after confirming it was clickable.")
    finally:
        driver.quit()


def fluent_wait_for_table_row():
    """Step 39: FluentWait polling every 500ms, max 10s, ignoring NoSuchElementException."""
    driver = build_driver(headless=False)
    try:
        driver.get(BASE_URL + "table-sort-search/")
        wait = FluentWebDriverWait(
            driver,
            timeout=10,
            poll_frequency=0.5,
            ignored_exceptions=[NoSuchElementException],
        )
        row = wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "table tbody tr"))
        print("First dynamically-loaded row found:", row.text[:60])
    finally:
        driver.quit()


if __name__ == "__main__":
    test_explicit_wait_for_alert()
    compare_sleep_vs_explicit_wait()
    test_element_to_be_clickable()
    fluent_wait_for_table_row()
