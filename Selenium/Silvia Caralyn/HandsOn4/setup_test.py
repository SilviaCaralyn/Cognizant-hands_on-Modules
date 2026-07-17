"""
HANDS-ON 4 - Task 1: Selenium Architecture and Environment Setup

Selenium Architecture (3 main components):

1. WebDriver:
   The core component. It is a set of language-specific bindings (Python, Java, etc.)
   that communicate directly with the browser via each browser's native automation API
   (e.g. Chrome's DevTools Protocol) through a browser driver executable (chromedriver).
   WebDriver sends commands (navigate, click, type) as HTTP requests to the driver,
   which translates them into native browser calls, and browser state is returned back.

2. Selenium Grid:
   Solves the problem of running tests in parallel across multiple machines and/or
   multiple browser/OS combinations. Instead of running all tests sequentially on one
   machine with one browser, Grid distributes test execution across a network of
   "nodes" (each with its own browser/OS), dramatically cutting total suite runtime
   for large regression suites.

3. Selenium IDE:
   A browser extension for record-and-playback test creation. A user performs actions
   in the browser (click, type, navigate) and Selenium IDE records them as a reusable
   test script. It can also export the recorded steps as code (e.g. Python + Selenium
   WebDriver boilerplate), useful for quickly bootstrapping a script or for
   non-programmers to get started with automation.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.lambdatest.com/selenium-playground/"


def build_driver(headless: bool = False):
    """Create and return a configured Chrome WebDriver instance."""
    options = Options()
    if headless:
        # Step 27: run without a visible browser window
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1280,800")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Step 26: implicit wait
    # NOTE: implicitly_wait() applies globally to EVERY find_element call for the
    # lifetime of the driver. This is considered bad practice because:
    #   1. It masks real timing issues instead of waiting for a *specific* condition
    #      (e.g. "element is clickable" vs just "element exists in the DOM").
    #   2. Mixing implicit waits with explicit WebDriverWait can cause unpredictable
    #      total wait times (the two can compound).
    #   3. It slows down failure detection: a genuinely-missing element still waits
    #      the full timeout before raising NoSuchElementException.
    # Explicit waits (Hands-On 5) let each wait target the exact condition needed,
    # per element, which is far more reliable and diagnosable.
    driver.implicitly_wait(10)
    return driver


def main():
    driver = build_driver(headless=False)
    try:
        driver.get(BASE_URL)
        print("Page title:", driver.title)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
