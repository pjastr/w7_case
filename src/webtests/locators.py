"""Locators as constants in ONE place.

Names of the constants are English; the values are the application's own
ids (Polish) – they are part of SklepTO and stay unchanged.
"""
from selenium.webdriver.common.by import By


class CalculatorPage:
    PATH = "/kalkulator.php"
    FORM = (By.ID, "form-kalkulator")
    VALUE = (By.ID, "wartosc")
    CARD = (By.ID, "karta")
    CODE = (By.ID, "kod")
    CALCULATE = (By.ID, "oblicz")
    CHECKED_DELIVERY = (By.CSS_SELECTOR, "input[name='dostawa']:checked")
    RESULT = (By.ID, "wynik")                  # only after a correct calculation
    DISCOUNT = (By.ID, "rabat")
    DELIVERY_COST = (By.ID, "koszt-dostawy")
    TO_PAY = (By.ID, "do-zaplaty")
    CODE_INFO = (By.ID, "kod-info")            # "Nieprawidłowy kod rabatowy…"
    ERRORS = (By.CSS_SELECTOR, "#bledy li.blad")

    @staticmethod
    def delivery(option: str) -> tuple[str, str]:
        """Radio button of a delivery option: kurier, paczkomat, odbior."""
        return By.ID, f"dostawa-{option}"


class WebFormPage:
    """Selenium Web Form – the practice page of the Selenium project."""
    PATH = "/web-form.html"
    SELECT = (By.NAME, "my-select")
