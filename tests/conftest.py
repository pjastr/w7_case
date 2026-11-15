"""Shared fixtures and hooks for all tests.

pytest finds this file by itself – the tests never import it.
"""
import os
import re

import pytest

from webtests.browser import create_driver
from webtests.calculator import Calculator
from webtests.config import SKLEPTO_URL, headless

# detailed assert messages also inside the helper module (not only in test files)
pytest.register_assert_rewrite("webtests.assertions")


def pytest_addoption(parser):
    """python -m pytest --headless – Chrome without a window (same as HEADLESS=1)."""
    parser.addoption("--headless", action="store_true",
                     help="run Chrome without a window (same as HEADLESS=1)")


def pytest_configure(config):
    if config.getoption("--headless"):
        os.environ["HEADLESS"] = "1"


def pytest_report_header(config):
    """First lines of the report: which application and browser mode the run used."""
    return f"SklepTO: {SKLEPTO_URL} | headless: {'yes' if headless() else 'no'}"


@pytest.fixture(scope="session")
def driver():
    """ONE browser for the whole run – the calculator keeps no state on the server.

    Unit tests (rules, pairwise …) do not ask for it, so no browser starts for them.
    """
    drv = create_driver()
    yield drv
    drv.quit()


@pytest.fixture
def calculator(driver):
    """The calculator page, freshly opened for every test."""
    return Calculator(driver).open()


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """After a failed 'call' phase of a browser test saves reports/screenshots/<test>.png."""
    report = yield
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv is not None:
            folder = item.config.rootpath / "reports" / "screenshots"
            folder.mkdir(parents=True, exist_ok=True)
            name = re.sub(r"[^\w.-]", "_", item.name) + ".png"   # [R1] -> _R1_ (Windows)
            try:
                drv.save_screenshot(str(folder / name))
            except Exception:   # e.g. a closed browser – the screenshot
                pass            # must not spoil the report
    return report
