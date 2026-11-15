"""Extended entries: the delivery option is ONE condition with three values (R-2, R-3).

Slides "Przykład wpisów rozszerzonych", "Wiele akcji – zbieranie niezgodności".
"""
import pytest

from webtests.assertions import check_actions
from webtests.calculator_tables import DELIVERY_FIELDS, DELIVERY_IDS, DELIVERY_TABLE

pytestmark = pytest.mark.ui


@pytest.mark.parametrize(DELIVERY_FIELDS, DELIVERY_TABLE, ids=DELIVERY_IDS)
def test_delivery(calculator, value, card, delivery, cost, to_pay):
    calculator.fill(value, card, delivery=delivery).calculate()
    actual = calculator.actions()
    check_actions(actual, {"delivery": cost, "to_pay": to_pay})   # all differences at once
