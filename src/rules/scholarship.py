"""Lecture example 1: scholarships.

S-1  Only a student who passed the year gets a scholarship.
S-2  Rector's scholarship: average >= 4.50 -> 1000 zł, 4.00–4.49 -> 600 zł, < 4.00 -> none.
S-3  Social scholarship: income per person <= 1500.00 zł.
S-4  Both scholarships can be granted at the same time.
"""
from decimal import Decimal


def scholarship(year_passed: bool, average: str, income: str) -> tuple[int, bool]:
    """(rector's scholarship in zł, social scholarship granted).

    Numbers come as text and are compared as Decimal – no float rounding at the
    boundaries 4.50 / 4.00 / 1500.00.
    """
    if not year_passed:
        return 0, False                            # S1
    avg = Decimal(average)
    if avg >= Decimal("4.50"):
        rector = 1000
    elif avg >= Decimal("4.00"):
        rector = 600
    else:
        rector = 0
    social = Decimal(income) <= Decimal("1500.00")
    return rector, social
