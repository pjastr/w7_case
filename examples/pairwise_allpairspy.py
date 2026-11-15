"""Lecture 7, slide "Pairwise – narzędzia": 4 parameters × 3 values.

    python examples/pairwise_allpairspy.py
All 3**4 = 81 combinations vs the pairwise set (about 9–10 tests).
"""
from allpairspy import AllPairs

parameters = [
    ["Chrome", "Firefox", "Edge"],        # browser
    ["Windows", "Linux", "macOS"],        # system
    ["PL", "EN", "DE"],                   # language
    ["karta", "BLIK", "przelew"],         # payment
]
for number, combination in enumerate(AllPairs(parameters), 1):
    print(number, combination)
