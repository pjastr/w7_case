"""Decision tables of the SklepTO calculator (requirements R-1 … R-4) as test data.

Conditions: W1 loyalty card, W2 value >= 200.00 zł, W3 correct code STUDENT10.
Actions:    A1 discount, A2 delivery cost, A3 amount to pay.
Expected actions are written BY HAND from the requirements (slide
"Wyrocznia: nie kopiuj logiki") – never computed with the application's formula.
Amounts are text: exactly what the page shows, no float rounding.
"""
CODE = "STUDENT10"

FULL_TABLE_FIELDS = "value, card, code, discount, delivery, to_pay"

# full table: 2**3 = 8 columns, all reachable; delivery: kurier (15.00 zł)
FULL_TABLE = [
    # value    card   code  discount delivery to_pay
    ("250.00", True,  CODE, "15%", "0.00",  "212.50"),  # R1 T T T
    ("250.00", True,  "",   "10%", "0.00",  "225.00"),  # R2 T T N
    ("100.00", True,  CODE, "15%", "0.00",  "85.00"),   # R3 T N T
    ("100.00", True,  "",   "10%", "0.00",  "90.00"),   # R4 T N N
    ("250.00", False, CODE, "10%", "0.00",  "225.00"),  # R5 N T T
    ("250.00", False, "",   "0%",  "0.00",  "250.00"),  # R6 N T N
    ("100.00", False, CODE, "10%", "15.00", "105.00"),  # R7 N N T
    ("100.00", False, "",   "0%",  "15.00", "115.00"),  # R8 N N N
]
FULL_TABLE_IDS = [f"R{i}" for i in range(1, len(FULL_TABLE) + 1)]

# extended entries (slide "Przykład wpisów rozszerzonych"): W2 = delivery option
DELIVERY_FIELDS = "value, card, delivery, cost, to_pay"
DELIVERY_TABLE = [
    # value    card   delivery     cost        to_pay
    ("100.00", True,  "paczkomat", "0.00 zł",  "90.00 zł"),    # E1 free (card)
    ("300.00", False, "odbior",    "0.00 zł",  "300.00 zł"),   # E2 free (>= 200)
    ("50.00",  False, "kurier",    "15.00 zł", "65.00 zł"),    # E3
    ("50.00",  False, "paczkomat", "10.00 zł", "60.00 zł"),    # E4
    ("50.00",  False, "odbior",    "0.00 zł",  "50.00 zł"),    # E5
]
DELIVERY_IDS = ["E1", "E2", "E3", "E4", "E5"]

ERROR_VALUE = "Wartość zamówienia musi być liczbą z zakresu 0,01–10000,00."
