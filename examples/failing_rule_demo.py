"""Lecture 7, slides "Który wiersz tablicy padł?" and "pytest.param – identyfikator przy danych".

discount_with_bug() mixes up the rules: card + purchase in 30 days gives 10%
even for an amount <= 1000 zł (column R3). Run it on purpose:
    python -m pytest examples/failing_rule_demo.py -v
Expected: test_discount[R3] FAILED (assert 10 == 5); in test_discount_param
the same column is marked xfail – XFAIL, the rest passes.
"""
import pytest


def discount_with_bug(card: bool, amount: float, recent_purchase: bool) -> int:
    if not card:
        return 0
    if amount > 1000 and recent_purchase or recent_purchase:   # DEFECT: R3 -> 10%
        return 10
    if amount > 1000:
        return 5
    return 0


DISCOUNT_TABLE = [
    # card   amount   30 days  discount
    (True,  1500.00, True,  10),   # R1  T T T
    (True,  1500.00, False, 5),    # R2  T T N
    (True,  800.00,  True,  5),    # R3  T N T
    (True,  800.00,  False, 0),    # R4  T N N
    (False, 1500.00, True,  0),    # R5  N – –
]


@pytest.mark.parametrize("card, amount, recent, expected", DISCOUNT_TABLE,
                         ids=["R1", "R2", "R3", "R4", "R5"])
def test_discount(card, amount, recent, expected):
    assert discount_with_bug(card, amount, recent) == expected


DISCOUNT_PARAMS = [
    pytest.param(True, 1500.00, True, 10, id="R1-TTT"),
    pytest.param(True, 1500.00, False, 5, id="R2-TTN"),
    pytest.param(True, 800.00, True, 5, id="R3-TNT",
                 marks=pytest.mark.xfail(reason="defect #42")),
    pytest.param(True, 800.00, False, 0, id="R4-TNN"),
    pytest.param(False, 1500.00, True, 0, id="R5-N--"),
]


@pytest.mark.parametrize("card, amount, recent, expected", DISCOUNT_PARAMS)
def test_discount_param(card, amount, recent, expected):
    assert discount_with_bug(card, amount, recent) == expected
