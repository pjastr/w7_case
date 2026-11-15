"""Textbook decision table (discount) as pytest tests – pure Python, no browser.

Slides "Tablica jako lista krotek", "Test parametryzowany",
"pytest.param – identyfikator przy danych", "Łączenie z EP i AWB".
"""
import pytest

from rules.decision_table import full_table
from rules.discount import discount

# minimised table: one tuple = one column
DISCOUNT_TABLE = [
    # card   amount   30 days  discount
    (True,  1500.00, True,  10),   # R1  T T T
    (True,  1500.00, False, 5),    # R2  T T N
    (True,  800.00,  True,  5),    # R3  T N T
    (True,  800.00,  False, 0),    # R4  T N N
    (False, 1500.00, True,  0),    # R5  N – –  ("–" filled with T: values tempting for buggy code)
]


@pytest.mark.parametrize("card, amount, recent, expected", DISCOUNT_TABLE,
                         ids=["R1", "R2", "R3", "R4", "R5"])
def test_discount(card, amount, recent, expected):
    assert discount(card, amount, recent) == expected


# the same table with the id right next to the data
DISCOUNT_PARAMS = [
    pytest.param(True, 1500.00, True, 10, id="R1-TTT"),
    pytest.param(True, 1500.00, False, 5, id="R2-TTN"),
    pytest.param(True, 800.00, True, 5, id="R3-TNT"),
    pytest.param(True, 800.00, False, 0, id="R4-TNN"),
    pytest.param(False, 1500.00, True, 0, id="R5-N--"),
]


@pytest.mark.parametrize("card, amount, recent, expected", DISCOUNT_PARAMS)
def test_discount_param(card, amount, recent, expected):
    assert discount(card, amount, recent) == expected


# full table: CONDITIONS generated with itertools.product, ACTIONS written by hand
EXPECTED_FULL = {
    # (card, amount > 1000, 30 days): discount – from the requirements
    (True, True, True): 10, (True, True, False): 5,
    (True, False, True): 5, (True, False, False): 0,
    (False, True, True): 0, (False, True, False): 0,
    (False, False, True): 0, (False, False, False): 0,
}
AMOUNT = {True: 1500.00, False: 800.00}   # a typical value of each class of W2


def tn(combination):
    """(True, False, True) -> 'TNT' – the column written as on the slide."""
    return "".join("T" if value else "N" for value in combination)


@pytest.mark.parametrize("card, over_1000, recent",
                         [pytest.param(*c, id=tn(c)) for c in full_table(3)])
def test_full_table(card, over_1000, recent):
    expected = EXPECTED_FULL[(card, over_1000, recent)]
    assert discount(card, AMOUNT[over_1000], recent) == expected


@pytest.mark.parametrize("amount, expected", [
    pytest.param(1000.00, 5, id="1000.00-N"),     # boundary: still "not more than 1000"
    pytest.param(1000.01, 10, id="1000.01-T"),    # the smallest value above it
])
def test_amount_threshold_bva(amount, expected):
    # card and purchase in 30 days fixed (T, T): only W2 changes
    assert discount(True, amount, True) == expected
