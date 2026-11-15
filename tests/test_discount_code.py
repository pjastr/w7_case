"""Condition W3 "correct code": letter case and invalid codes (equivalence classes)."""
import pytest

pytestmark = pytest.mark.ui


@pytest.mark.parametrize("code", ["STUDENT10", "student10", "Student10"])
def test_valid_code(calculator, code):
    calculator.fill("100.00", code=code).calculate()
    assert calculator.result() == ("10%", "15.00 zł", "105.00 zł")
    assert not calculator.has_code_info()


@pytest.mark.parametrize("code", ["STUDENT11", "STUDENT1", "STUDENT100", "STUDENT 10"])
def test_invalid_code(calculator, code):
    calculator.fill("100.00", code=code).calculate()
    assert calculator.result() == ("0%", "15.00 zł", "115.00 zł")
    assert calculator.has_code_info()


def test_empty_code_without_message(calculator):
    calculator.fill("100.00", code="").calculate()
    assert calculator.result()[0] == "0%"
    assert not calculator.has_code_info()
