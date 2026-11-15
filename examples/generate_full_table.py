"""Lecture 7, slides "Systematyczne wypełnianie" and "Drzewo kombinacji".

    python examples/generate_full_table.py
itertools.product generates the CONDITIONS of a full table – never the expected actions.
"""
from itertools import product

# limited entries: 3 conditions T/N -> 2**3 = 8 columns, "halving" order
columns = list(product("TN", repeat=3))
for row in range(3):
    print(f"W{row + 1}:", " ".join(column[row] for column in columns))

# extended entries: income {M, D} × age {MŁ, ŚR, ST} × place {MI, W} -> 2 × 3 × 2 = 12
leaves = list(product(["M", "D"], ["MŁ", "ŚR", "ST"], ["MI", "W"]))
for number, leaf in enumerate(leaves, 1):
    print(f"({number})", *leaf)
print("columns:", len(leaves))
