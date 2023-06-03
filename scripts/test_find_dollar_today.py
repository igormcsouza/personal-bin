"""
Test getDollar main function
"""
import os
from unittest.mock import patch
from datetime import datetime, timedelta

from freezegun import freeze_time

import find_dollar_today
from find_dollar.sources.open_exchange import RetrieveRateOpenExchange


def assert_equals(test, real):
    assert test == real


def assert_almost_equals(test, real, precision=3):
    assert round(test, precision) == round(real, precision)


@freeze_time("2023-01-01")
@patch("find_dollar.sources.open_exchange.RetrieveRateOpenExchange.get_today")
@patch("find_dollar.sources.open_exchange.RetrieveRateOpenExchange.get_before")
def test_executes_correctly(get_before, get_today):
    get_today.return_value = 5.20
    get_before.return_value = 5.20

    source = RetrieveRateOpenExchange("something")
    dates = [
        datetime.now() - timedelta(days=5),  # Five days ago
        datetime.now().replace(day=1),  # First day of the actual month
        datetime.now() - timedelta(days=30)  # One month Ago
    ]

    rate, five_days, first_month_day, one_month = find_dollar_today.get_results(source, dates)

    get_today.assert_called()
    get_before.assert_called()

    assert_equals(rate, 5.20)
    assert_equals(five_days, 0)
    assert_equals(first_month_day, 0)
    assert_equals(one_month, 0)


def get_before_side_effect(date_obj=None):
    if date_obj:
        if date_obj.day == 5:
            return 5.15
        elif date_obj.day == 11:
            return 5.25
        elif date_obj.day == 1:
            return 5.10

    return 5.20

def get_today_side_effect():
    return 5.20


@freeze_time("2023-01-10")
@patch("find_dollar.sources.open_exchange.RetrieveRateOpenExchange.get_today")
@patch("find_dollar.sources.open_exchange.RetrieveRateOpenExchange.get_before")
def test_calculates_correctly(get_before, get_today):
    get_before.side_effect = get_before_side_effect
    get_today.side_effect = get_today_side_effect

    source = RetrieveRateOpenExchange("something")
    dates = [
        datetime.now() - timedelta(days=5),  # Five days ago
        datetime.now().replace(day=1),  # First day of the actual month
        datetime.now() - timedelta(days=30)  # One month Ago
    ]

    rate, five_days, first_month_day, one_month = find_dollar_today.get_results(source, dates)

    get_today.assert_called()
    get_before.assert_called()

    assert_equals(rate, 5.20)
    assert_almost_equals(five_days, 0.97, 2)
    assert_almost_equals(first_month_day, 1.96, 2)
    assert_almost_equals(one_month, -0.95, 2)

