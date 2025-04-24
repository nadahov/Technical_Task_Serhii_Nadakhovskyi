# utils/driver_factory.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def get_driver(browser_name="chrome"):
    """
    Returns a WebDriver instance for the specified browser.
    Supported browsers: 'chrome', 'firefox'
    """
    if browser_name.lower() == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        return webdriver.Chrome(service=ChromeService(), options=options)

    elif browser_name.lower() == "firefox":
        options = FirefoxOptions()
        options.add_argument("--start-maximized")
        return webdriver.Firefox(service=FirefoxService(), options=options)

    else:
        raise ValueError("Only 'chrome' or 'firefox' are supported")