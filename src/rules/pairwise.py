"""Pairwise testing: which pairs of values a set of tests does not cover."""
from itertools import combinations, product


def uncovered_pairs(rows: list[tuple], values: list[list]) -> list[tuple]:
    """[(i, j, value_i, value_j), …] – pairs of parameters i < j never tested together.

    rows   – the tests, one tuple of parameter values each,
    values – the possible values of every parameter.
    """
    missing = []
    for i, j in combinations(range(len(values)), 2):
        tested = {(row[i], row[j]) for row in rows}
        missing += [(i, j, a, b) for a, b in product(values[i], values[j])
                    if (a, b) not in tested]
    return missing
