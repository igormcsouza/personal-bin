"""
Test getDollar main function
"""
from unittest.mock import patch
from datetime import datetime

from freezegun import freeze_time

import find_dollar_today


def assert_equals(test, real):
    assert test == real


def assert_almost_equals(test, real, precision=3):
    assert round(test, precision) == round(real, precision)


@freeze_time("2023-01-01")
@patch("forex_python.converter.CurrencyRates.get_rate")
def test_executes_correctly(get_rate):
    get_rate.return_value = 5.20
    rate, five_days, first_month_day, one_month = find_dollar_today.main()

    get_rate.assert_called()

    assert_equals(rate, 5.20)
    assert_equals(five_days, 0)
    assert_equals(first_month_day, 0)
    assert_equals(one_month, 0)

def get_rate_side_effect(base, simbol, date_obj=None):
    if date_obj:
        if date_obj.day == 5:
            return 5.15
        elif date_obj.day == 11:
            return 5.25
        elif date_obj.day == 1:
            return 5.10

    return 5.20

@freeze_time("2023-01-10")
@patch("forex_python.converter.CurrencyRates.get_rate")
def test_calculates_correctly(get_rate):
    get_rate.side_effect = get_rate_side_effect

    rate, five_days, first_month_day, one_month = find_dollar_today.main()

    get_rate.assert_called()

    assert_equals(rate, 5.20)
    assert_almost_equals(five_days, 0.97, 2)
    assert_almost_equals(first_month_day, 1.96, 2)
    assert_almost_equals(one_month, -0.95, 2)

