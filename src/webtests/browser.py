"""One place that creates the browser – tests never call webdriver.Chrome() directly."""
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from webtests.config import WINDOW_SIZE, headless as headless_from_config


def create_driver(headless: bool | None = None) -> WebDriver:
    """Starts Chrome with the same options for every test run.

    Selenium Manager downloads a matching chromedriver – no admin rights needed.
    """
    if headless is None:
        headless = headless_from_config()   # --headless or HEADLESS=1
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")            # no window
    options.add_argument(f"--window-size={WINDOW_SIZE}")   # fixed size = stable layout
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(0)   # explicit waits only (lecture 5)
    return driver
