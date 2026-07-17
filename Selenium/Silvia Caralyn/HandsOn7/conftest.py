"""
HANDS-ON 6: Shared pytest fixtures for the Selenium Playground suite.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# Step 48: session-scoped base_url constant
@pytest.fixture(scope="session")
def base_url():
    return "https://www.lambdatest.com/selenium-playground/"


# Step 41: driver fixture, function scope -> fresh browser per test
@pytest.fixture(scope="function")
def driver():
    options = Options()
    # Uncomment for headless CI runs:
    # options.add_argument("--headless=new")
    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    drv.implicitly_wait(5)
    drv.maximize_window()

    yield drv  # --- setup above, teardown below ---

    drv.quit()


# Step 46: screenshot on failure hook
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # find the 'driver' fixture instance if the test used one
        drv = item.funcargs.get("driver")
        if drv is not None:
            test_name = item.name.replace(" ", "_").replace(":", "_")
            try:
                drv.save_screenshot(f"{test_name}_failure.png")
                print(f"\nScreenshot captured: {test_name}_failure.png")
            except Exception as e:
                print(f"\nCould not capture screenshot: {e}")
