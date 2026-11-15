"""Lecture 7, slide "Wyrocznia: nie kopiuj logiki" – an ANTI-PATTERN, kept for comparison.

The developer misread R-1 and ADDED the discounts (card 10% + code 10% = 20%).
test_discount_copied computes the expected value with the same wrong idea
and passes; test_discount_from_requirements has the values written by hand
from R-1 and finds the defect. Run it on purpose:
    python -m pytest examples/anti_pattern_copied_oracle.py -v
Expected: 4 passed (copied oracle) and test_discount_from_requirements[T-T] FAILED.
"""
import itertools

import pytest


def calculator_discount(card: bool, code_ok: bool) -> int:
    """Implementation with a misunderstanding: the discounts are summed."""
    return (10 if card else 0) + (10 if code_ok else 0)


@pytest.mark.parametrize("card, code_ok",
                         list(itertools.product([True, False], repeat=2)))
def test_discount_copied(card, code_ok):
    expected = (10 if card else 0) + (10 if code_ok else 0)   # a copy of the implementation!
    assert calculator_discount(card, code_ok) == expected


R1_EXPECTED = {   # from R-1: both -> 15%, one of them -> 10%, none -> 0%
    (True, True): 15, (True, False): 10, (False, True): 10, (False, False): 0,
}


@pytest.mark.parametrize("card, code_ok", list(R1_EXPECTED),
                         ids=["T-T", "T-N", "N-T", "N-N"])
def test_discount_from_requirements(card, code_ok):
    assert calculator_discount(card, code_ok) == R1_EXPECTED[(card, code_ok)]
