"""BVA: the free-delivery threshold (200.00 zł) and the value range R-4.

Slides "Łączenie z EP i AWB", "Przykład: próg darmowej dostawy", "Ile testów łącznie?".
The threshold is tested WITHOUT the card – the card alone gives free delivery
and would hide condition W2.
"""
import pytest

from webtests.calculator_tables import ERROR_VALUE
from webtests.locators import CalculatorPage as Page

pytestmark = pytest.mark.ui


@pytest.mark.parametrize("value, delivery, to_pay", [
    pytest.param("199.99", "15.00 zł", "214.99 zł", id="199.99-below"),
    pytest.param("200.00", "0.00 zł", "200.00 zł", id="200.00-on"),
    pytest.param("200.01", "0.00 zł", "200.01 zł", id="200.01-above"),
    pytest.param("199,99", "15.00 zł", "214.99 zł", id="199,99-comma"),
    pytest.param("200,00", "0.00 zł", "200.00 zł", id="200,00-comma"),
])
def test_free_delivery_threshold(calculator, value, delivery, to_pay):
    calculator.fill(value).calculate()
    assert calculator.result() == ("0%", delivery, to_pay)


@pytest.mark.parametrize("value, to_pay", [
    pytest.param("0.01", "15.01 zł", id="min"),
    pytest.param("10000.00", "10000.00 zł", id="max"),
])
def test_valid_range(calculator, value, to_pay):
    calculator.fill(value).calculate()
    assert calculator.errors() == []
    assert calculator.text(Page.TO_PAY) == to_pay


@pytest.mark.parametrize("value", [
    "0.00", "10000.01",            # just outside the range
    "-5", "abc", "", "12.345",     # other invalid classes
])
def test_invalid_range(calculator, value):
    calculator.fill(value).calculate()
    assert calculator.errors() == [ERROR_VALUE]
    assert not calculator.has_result()
