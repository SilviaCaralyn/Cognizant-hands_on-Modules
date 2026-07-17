"""
HANDS-ON 4 - Task 2: WebDriver Navigation and Window Commands
"""

from selenium.webdriver.common.by import By
from setup_test import build_driver, BASE_URL


def main():
    driver = build_driver(headless=False)
    try:
        # Step 28: navigate to Simple Form Demo, assert URL, go back
        driver.get(BASE_URL)
        simple_form_link = driver.find_element(By.LINK_TEXT, "Simple Form Demo")
        simple_form_link.click()
        assert "simple-form-demo" in driver.current_url, "URL did not navigate as expected"
        print("Navigated to Simple Form Demo:", driver.current_url)
        driver.back()
        print("Navigated back to:", driver.current_url)

        # Step 29: open a new tab, switch to it, print its title
        driver.execute_script('window.open("https://www.google.com");')
        all_handles = driver.window_handles
        print("Open tabs:", len(all_handles))
        driver.switch_to.window(all_handles[1])
        print("New tab title:", driver.title)

        # Step 30: switch back to original tab and take a screenshot
        driver.switch_to.window(all_handles[0])
        driver.save_screenshot("playground_screenshot.png")
        print("Screenshot saved: playground_screenshot.png")

        # Step 31: window size
        print("Current window size:", driver.get_window_size())
        driver.set_window_size(1280, 800)
        print("New window size:", driver.get_window_size())
        # Consistent window size matters because responsive web apps render
        # different layouts (and sometimes different DOM elements/locators)
        # at different viewport widths. A test that passes at one window
        # size may fail at another due to elements moving, collapsing into
        # a hamburger menu, or becoming hidden/overlapped — so fixing the
        # size makes automation results reproducible across runs/machines.

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
