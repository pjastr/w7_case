"""Textbook example: discount in a shop (Roman, Stapp, Pilaeten, Helion 2024, tab. 4.4).

Conditions: W1 loyalty card, W2 amount > 1000 zł, W3 purchase in the last 30 days.
Action:     A1 discount in %.
"""


def discount(card: bool, amount: float, recent_purchase: bool) -> int:
    """Discount in % for one combination of conditions."""
    if not card:
        return 0                                   # R5': without a card always 0%
    if amount > 1000 and recent_purchase:
        return 10                                  # R1
    if amount > 1000 or recent_purchase:
        return 5                                   # R2, R3
    return 0                                       # R4
