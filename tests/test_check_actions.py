"""check_actions(): several actions of one rule, all differences in one message.

Slide "Wiele akcji – zbieranie niezgodności".
"""
import pytest

from webtests.assertions import check_actions


def test_equal_actions_pass():
    check_actions({"discount": "10%", "delivery": "0.00 zł"},
                  {"discount": "10%", "delivery": "0.00 zł"})


def test_all_differences_are_reported():
    with pytest.raises(AssertionError) as error:
        check_actions({"discount": "0%", "delivery": "15.00 zł"},
                      {"discount": "10%", "delivery": "0.00 zł"})
    message = str(error.value)
    assert "discount: is '0%', expected '10%'" in message
    assert "delivery: is '15.00 zł', expected '0.00 zł'" in message
