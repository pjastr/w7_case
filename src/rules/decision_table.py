"""Minimised decision tables: "–" (don't care) and the coverage check.

A rule is a tuple of condition values: True (T), False (N) or DONT_CARE ("–").
Slide "Kontrola poprawności minimalizacji": every "–" stands for 2 columns of
the full table, so the expanded rules must give each of the 2**n combinations
exactly once.
"""
from itertools import product

DONT_CARE = None   # "–" – the value of the condition does not change the actions


def expand(rule: tuple) -> list[tuple]:
    """All full combinations hidden behind a rule, e.g. (F, –, –) -> 4 combinations."""
    options = [(True, False) if value is DONT_CARE else (value,) for value in rule]
    return list(product(*options))


def full_table(n: int) -> list[tuple]:
    """All 2**n combinations in the "halving" order: T T T, T T N, …, N N N."""
    return list(product([True, False], repeat=n))


def check_minimised(rules: list[tuple]) -> tuple[list[tuple], list[tuple]]:
    """(missing, repeated) combinations of a minimised table.

    missing  – a gap: no rule covers the combination,
    repeated – rules overlap (possible contradiction).
    """
    n = len(rules[0])
    seen = [combination for rule in rules for combination in expand(rule)]
    missing = [c for c in full_table(n) if c not in seen]
    repeated = sorted({c for c in seen if seen.count(c) > 1}, reverse=True)
    return missing, repeated
