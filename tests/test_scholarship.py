"""Lecture example 1: scholarships – test cases with boundary values woven in.

Slides "Przykład 1: tablica zminimalizowana", "Przykład 1: dane testowe z AWB".
"""
import pytest

from rules.scholarship import scholarship


@pytest.mark.parametrize("year, average, income, expected", [
    pytest.param(False, "4.80", "900.00", (0, False), id="TC1-S1"),
    pytest.param(True, "4.50", "1500.00", (1000, True), id="TC2-S2"),
    pytest.param(True, "4.93", "1500.01", (1000, False), id="TC3-S3"),
    pytest.param(True, "4.00", "1200.00", (600, True), id="TC4-S4"),
    pytest.param(True, "4.49", "3000.00", (600, False), id="TC5-S5"),
    pytest.param(True, "3.99", "1000.00", (0, True), id="TC6-S6"),
    pytest.param(True, "3.20", "2000.00", (0, False), id="TC7-S7"),
])
def test_scholarship(year, average, income, expected):
    assert scholarship(year, average, income) == expected
