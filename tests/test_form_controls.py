"""Form controls in Selenium: text field, checkbox, radio, select, submit and wait.

Slides "Pole tekstowe", "Pole wyboru (checkbox)", "Przyciski opcji (radio)",
"Lista rozwijana (select)", "Wysłanie formularza i oczekiwanie".
"""
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from webtests.config import SELENIUM_WEB_URL, SKLEPTO_URL, TIMEOUT
from webtests.locators import CalculatorPage as Page
from webtests.locators import WebFormPage

pytestmark = pytest.mark.ui


@pytest.fixture
def page(driver):
    driver.get(f"{SKLEPTO_URL}{Page.PATH}")
    return driver


def test_text_field_clear_and_type(page):
    field = page.find_element(*Page.VALUE)
    field.send_keys("250")
    field.send_keys("199,99")                      # without clear() – appended
    assert field.get_attribute("value") == "250199,99"
    field.clear()                                  # remove the previous value
    field.send_keys("199,99")
    assert field.get_attribute("value") == "199,99"
    assert field.text == ""                        # .text of an <input> is empty


def test_checkbox_click_toggles(page):
    checkbox = page.find_element(*Page.CARD)
    assert not checkbox.is_selected()
    checkbox.click()
    assert checkbox.is_selected()
    checkbox.click()                               # the second click unchecks it
    assert not checkbox.is_selected()


@pytest.mark.parametrize("card", [True, False], ids=["card", "no-card"])
def test_checkbox_set_state(page, card):
    checkbox = page.find_element(*Page.CARD)
    if checkbox.is_selected() != card:             # card: True / False
        checkbox.click()                           # click only when needed
    assert checkbox.is_selected() == card


def test_checkbox_state_remembered_after_reload(calculator, driver):
    calculator.fill("100.00", card=True).calculate()
    # the form remembers the value – never assume the initial state
    assert driver.find_element(*Page.CARD).is_selected()


def test_radio_group(page):
    page.find_element(*Page.delivery("paczkomat")).click()
    chosen = page.find_element(*Page.CHECKED_DELIVERY)
    assert chosen.get_attribute("value") == "paczkomat"
    assert not page.find_element(*Page.delivery("kurier")).is_selected()
    page.find_element(*Page.delivery("paczkomat")).click()   # clicking again …
    assert page.find_element(*Page.delivery("paczkomat")).is_selected()   # … does not uncheck


def test_select_on_web_form(driver):
    driver.get(f"{SELENIUM_WEB_URL}{WebFormPage.PATH}")
    dropdown = Select(driver.find_element(*WebFormPage.SELECT))
    dropdown.select_by_visible_text("Two")
    assert dropdown.first_selected_option.text == "Two"
    dropdown.select_by_value("3")
    assert dropdown.first_selected_option.get_attribute("value") == "3"


def test_submit_and_wait_for_new_page(page):
    page.find_element(*Page.VALUE).send_keys("100.00")
    button = page.find_element(*Page.CALCULATE)
    button.click()
    # the GET form reloads the page – wait for the new one
    WebDriverWait(page, TIMEOUT).until(EC.staleness_of(button))
    assert page.find_element(*Page.TO_PAY).text == "115.00 zł"
