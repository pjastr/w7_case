"""Minimised table: "–" (don't care), the 2**n check and the risk of "–".

Slides "Minimalizacja krok po kroku", "Kontrola poprawności minimalizacji",
"Minimalizacja – ryzyko".
"""
from rules.decision_table import DONT_CARE as X
from rules.decision_table import check_minimised, expand, full_table
from rules.discount import discount

T, N = True, False

MINIMISED = {
    # (card, amount > 1000, 30 days): discount
    (T, T, T): 10,   # R1
    (T, T, N): 5,    # R2
    (T, N, T): 5,    # R3
    (T, N, N): 0,    # R4
    (N, X, X): 0,    # R5' – without a card always 0%
}


def test_full_table_halving_order():
    rows = full_table(3)
    assert len(rows) == 2 ** 3
    assert [row[0] for row in rows] == [T, T, T, T, N, N, N, N]   # W1: half T, half N
    assert [row[2] for row in rows] == [T, N, T, N, T, N, T, N]   # W3: alternating


def test_dash_stands_for_two_columns():
    assert expand((N, X, X)) == [(N, T, T), (N, T, N), (N, N, T), (N, N, N)]   # 2**2


def test_minimised_table_has_no_gaps_and_no_overlaps():
    missing, repeated = check_minimised(list(MINIMISED))
    assert missing == []         # 1 + 1 + 1 + 1 + 4 = 8 = 2**3
    assert repeated == []


def test_missing_rule_is_a_gap():
    rules = [r for r in MINIMISED if r != (T, N, N)]
    assert check_minimised(rules) == ([(T, N, N)], [])


def test_overlapping_rules_are_detected():
    rules = list(MINIMISED) + [(T, X, T)]          # covers R1 and R3 again
    assert check_minimised(rules) == ([], [(T, T, T), (T, N, T)])


def test_implementation_agrees_with_every_hidden_column():
    # "–" is an ASSUMPTION – check every combination behind it, not only one
    amount = {T: 1500.00, N: 800.00}
    for rule, expected in MINIMISED.items():
        for card, over_1000, recent in expand(rule):
            assert discount(card, amount[over_1000], recent) == expected, rule
