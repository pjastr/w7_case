"""Pairwise: every pair of values of any two parameters in at least one test.

Slides "Pairwise – przykład", "Pairwise – narzędzia".
"""
from allpairspy import AllPairs

from rules.pairwise import uncovered_pairs

T, N = True, False
BOOL3 = [[T, N]] * 3                # three conditions A, B, C

PAIRWISE_4 = [(T, T, T), (T, N, N), (N, T, N), (N, N, T)]

PARAMETERS = [
    ["Chrome", "Firefox", "Edge"],        # browser
    ["Windows", "Linux", "macOS"],        # system
    ["PL", "EN", "DE"],                   # language
    ["karta", "BLIK", "przelew"],         # payment
]


def test_four_tests_cover_all_pairs():
    assert uncovered_pairs(PAIRWISE_4, BOOL3) == []


def test_pairwise_misses_a_combination():
    assert (T, T, N) not in PAIRWISE_4    # a defect only in (T, T, N) is not found


def test_three_tests_are_not_enough():
    assert uncovered_pairs(PAIRWISE_4[:3], BOOL3) != []


def test_allpairspy_covers_all_pairs_with_few_tests():
    rows = [tuple(row) for row in AllPairs(PARAMETERS)]
    assert uncovered_pairs(rows, PARAMETERS) == []
    assert len(rows) <= 10 < 3 ** 4                # instead of 81 combinations
