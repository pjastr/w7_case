"""Full decision table of the calculator through the UI: one column = one test.

Slides "Przykład 3: kalkulator SklepTO", "Asercja wielu akcji",
"Klasa pomocnicza dla formularza".
"""
import pytest

from webtests.calculator_tables import FULL_TABLE, FULL_TABLE_FIELDS, FULL_TABLE_IDS

pytestmark = pytest.mark.ui


@pytest.mark.parametrize(FULL_TABLE_FIELDS, FULL_TABLE, ids=FULL_TABLE_IDS)
def test_rule(calculator, value, card, code, discount, delivery, to_pay):
    calculator.fill(value, card, code).calculate()
    # all actions of the rule in ONE assert on a tuple
    expected = (discount, f"{delivery} zł", f"{to_pay} zł")
    assert calculator.result() == expected
