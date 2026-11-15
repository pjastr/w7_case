"""Helper class for kalkulator.php – a preview of the Page Object pattern (lecture 9).

Filling in the form repeats in every test, so it lives in ONE place.
Every method that does something returns self, so calls can be chained:
    calculator.open().fill("250.00", True, "STUDENT10").calculate()
"""
from urllib.parse import urlencode

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from webtests.config import SKLEPTO_URL, TIMEOUT
from webtests.locators import CalculatorPage as Page


def calculator_url(value: str, card: bool = False, code: str = "",
                   delivery: str = "kurier") -> str:
    """The same request as the form sends (method GET) – urlencode() encodes & and spaces."""
    params = {"wartosc": value, "kod": code, "dostawa": delivery, "oblicz": "1"}
    if card:
        params["karta"] = "1"          # an unchecked checkbox is not sent at all
    return f"{SKLEPTO_URL}{Page.PATH}?{urlencode(params)}"


class Calculator:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        # while the page reloads Chrome may raise a generic WebDriverException
        # instead of "stale element" – the wait ignores it and asks again
        self.wait = WebDriverWait(driver, TIMEOUT, ignored_exceptions=[WebDriverException])

    def open(self) -> "Calculator":
        self.driver.get(f"{SKLEPTO_URL}{Page.PATH}")
        return self

    def fill(self, value: str, card: bool = False, code: str = "",
             delivery: str = "kurier") -> "Calculator":
        field = self.driver.find_element(*Page.VALUE)
        field.clear()                              # without clear() the text is appended
        field.send_keys(value)
        checkbox = self.driver.find_element(*Page.CARD)
        if checkbox.is_selected() != card:
            checkbox.click()                       # click only when needed
        code_field = self.driver.find_element(*Page.CODE)
        code_field.clear()
        code_field.send_keys(code)
        self.driver.find_element(*Page.delivery(delivery)).click()
        return self

    def calculate(self) -> "Calculator":
        button = self.driver.find_element(*Page.CALCULATE)
        button.click()
        # the GET form reloads the page – wait until the old button is gone
        self.wait.until(EC.staleness_of(button), message="the page did not reload")
        return self

    def text(self, locator: tuple[str, str]) -> str:
        return self.driver.find_element(*locator).text

    def result(self) -> tuple[str, str, str]:
        """(discount, delivery cost, to pay) – texts from the page."""
        return (self.text(Page.DISCOUNT), self.text(Page.DELIVERY_COST),
                self.text(Page.TO_PAY))

    def actions(self) -> dict[str, str]:
        """The same actions as a dict – for check_actions()."""
        discount, delivery, to_pay = self.result()
        return {"discount": discount, "delivery": delivery, "to_pay": to_pay}

    def errors(self) -> list[str]:
        return [li.text for li in self.driver.find_elements(*Page.ERRORS)]

    def has_result(self) -> bool:
        return len(self.driver.find_elements(*Page.RESULT)) > 0

    def has_code_info(self) -> bool:
        return len(self.driver.find_elements(*Page.CODE_INFO)) > 0
