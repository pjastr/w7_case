"""The same rules without the form: a GET address with parameters.

Slide "Test przez UI czy przez URL?". Timing: python -m pytest tests/test_get_vs_ui.py -rP
"""
import time

import pytest

from webtests.calculator import Calculator, calculator_url
from webtests.calculator_tables import FULL_TABLE, FULL_TABLE_FIELDS, FULL_TABLE_IDS

pytestmark = pytest.mark.ui


@pytest.mark.parametrize(FULL_TABLE_FIELDS, FULL_TABLE, ids=FULL_TABLE_IDS)
def test_rule_via_url(driver, value, card, code, discount, delivery, to_pay):
    driver.get(calculator_url(value, card, code))
    expected = (discount, f"{delivery} zł", f"{to_pay} zł")
    assert Calculator(driver).result() == expected


def test_ui_and_url_give_the_same_results(driver):
    calculator = Calculator(driver)
    start = time.perf_counter()                # a clock for measuring durations
    via_ui = []
    for value, card, code, *_ in FULL_TABLE:
        calculator.open().fill(value, card, code).calculate()
        via_ui.append(calculator.result())
    ui_seconds = time.perf_counter() - start

    start = time.perf_counter()
    via_url = []
    for value, card, code, *_ in FULL_TABLE:
        driver.get(calculator_url(value, card, code))
        via_url.append(calculator.result())
    url_seconds = time.perf_counter() - start

    print(f"\nUI: {ui_seconds:.2f} s, URL: {url_seconds:.2f} s")
    assert via_ui == via_url                   # both ways give the same result
