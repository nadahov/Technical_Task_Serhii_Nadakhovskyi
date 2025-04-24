# tests/conftest.py

import os
import glob
import pytest
from utils.driver_factory import get_driver

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """Delete all .png screenshots in /tests/screenshots before test session starts."""
    screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    for f in glob.glob(os.path.join(screenshot_dir, "*.png")):
        try:
            os.remove(f)
        except Exception as e:
            print(f"⚠️ Could not delete {f}: {e}")

_driver_store = {}

@pytest.fixture
def driver(request):
    browser = request.param
    driver = get_driver(browser)
    _driver_store[request.node.nodeid] = driver
    yield driver
    driver.quit()
    _driver_store.pop(request.node.nodeid, None)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # This is the correct pattern for wrapping hooks
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = _driver_store.get(item.nodeid)
        if driver:
            screenshot_name = f"screenshot_{item.name}.png"
            driver.save_screenshot(screenshot_name)
            print(f"📸 Screenshot captured: {screenshot_name}")