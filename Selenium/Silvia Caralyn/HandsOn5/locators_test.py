"""
HANDS-ON 5 - Task 1: Locator Strategies — From Simple to Robust

Ranking of the 6 locator strategies, most to least preferred (see comments
at the bottom for justification).
"""

from selenium.webdriver.common.by import By
from setup_test import build_driver, BASE_URL


def demo_simple_form_locators():
    driver = build_driver(headless=False)
    try:
        driver.get(BASE_URL + "simple-form-demo/")

        # Step 32: locate the message input field using all 6 strategies
        by_id = driver.find_element(By.ID, "user-message")
        by_name = driver.find_element(By.NAME, "message")
        by_class = driver.find_element(By.CLASS_NAME, "form-control")
        by_tag = driver.find_element(By.TAG_NAME, "input")
        by_xpath_absolute = driver.find_element(
            By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div/form/div[1]/input"
        )
        by_xpath_relative = driver.find_element(By.XPATH, "//input[@id='user-message']")

        for label, el in [
            ("By.ID", by_id),
            ("By.NAME", by_name),
            ("By.CLASS_NAME", by_class),
            ("By.TAG_NAME", by_tag),
            ("By.XPATH (absolute)", by_xpath_absolute),
            ("By.XPATH (relative)", by_xpath_relative),
        ]:
            print(f"{label}: found = {el is not None}")

        # Step 33: 3 different CSS selectors for the same element
        css_by_id = driver.find_element(By.CSS_SELECTOR, "#user-message")
        css_by_attr = driver.find_element(By.CSS_SELECTOR, "[name='message']")
        css_by_parent_child = driver.find_element(By.CSS_SELECTOR, "div.form-group > input#user-message")
        print("CSS by ID found:", css_by_id is not None)
        print("CSS by attribute found:", css_by_attr is not None)
        print("CSS by parent > child found:", css_by_parent_child is not None)

    finally:
        driver.quit()


def demo_checkbox_locators():
    driver = build_driver(headless=False)
    try:
        driver.get(BASE_URL + "checkbox-demo/")

        # Step 34: XPath text() and contains()
        exact_match = driver.find_element(By.XPATH, "//label[text()='Option 1']")
        contains_matches = driver.find_elements(By.XPATH, "//label[contains(text(),'Option')]")
        print("Exact text() match found:", exact_match is not None)
        print("contains() matches found:", len(contains_matches))

    finally:
        driver.quit()


# Step 35: Ranking locator strategies (most -> least preferred)
#
# 1. By.ID              - Unique, fast, and stable; the gold standard when present.
# 2. By.CSS_SELECTOR     - Fast, readable, and expressive for attributes/hierarchy;
#                          generally faster than XPath in most browsers.
# 3. By.NAME             - Usually unique on forms, readable, reasonably stable.
# 4. By.XPATH (relative, - Powerful (supports text()/contains()/axes) but more
#    attribute-based)      verbose and slightly slower than CSS; use when CSS can't
#                          express the condition (e.g., matching by visible text).
# 5. By.CLASS_NAME /      - Classes are often shared by many elements (styling
#    By.TAG_NAME            classes reused across the page) and tags are almost
#                          never unique alone — both are brittle as sole locators.
# 6. By.XPATH (absolute)  - Least preferred. Tied directly to the exact DOM tree
#                          structure; breaks with any structural HTML change,
#                          even ones unrelated to the target element.


if __name__ == "__main__":
    demo_simple_form_locators()
    demo_checkbox_locators()
