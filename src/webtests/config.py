"""Application URLs and browser settings.

Every value can be overridden with an environment variable
(PyCharm: Run ▸ Edit Configurations ▸ Environment variables),
so a different port or host never requires changing the code.
"""
import os

SKLEPTO_URL = os.getenv("SKLEPTO_URL", "http://localhost/sklepto").rstrip("/")
SELENIUM_WEB_URL = os.getenv("SELENIUM_WEB_URL", "https://www.selenium.dev/selenium/web").rstrip("/")
WINDOW_SIZE = os.getenv("WINDOW_SIZE", "1280,900")     # the layout depends on it
TIMEOUT = float(os.getenv("TIMEOUT", "10"))            # ONE limit for explicit waits


def headless() -> bool:
    """HEADLESS=1 – no browser window.

    Read on every call (not once at import), so the --headless option
    from tests/conftest.py can still switch it on.
    """
    return os.getenv("HEADLESS", "0") == "1"
