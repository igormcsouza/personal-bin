import argparse
from datetime import datetime, timedelta
from typing import Type
import time

from find_dollar.utils import print_results
from find_dollar.database import DataModel, insert_one, create_tables
from find_dollar.sources.abstract import RetrieveRateAbstract
from find_dollar.sources.open_exchange import RetrieveRateOpenExchange


def get_results(source: Type[RetrieveRateAbstract], dates=list[datetime]):
    today_rate = source.get_today()
    rates = [today_rate]

    for d in dates:
        the_rate = source.get_before(d)
        rates.append(((today_rate - the_rate) / the_rate) * 100)

    return rates


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--appid')
    parser.add_argument('-c', '--cache', help="Choose how long the cache can be used")
    args = parser.parse_args()

    create_tables()

    source = RetrieveRateOpenExchange(args.appid)  # Using OpenExchangeAPI source
    dates = [
        datetime.now() - timedelta(days=5),  # Five days ago
        datetime.now().replace(day=1),  # First day of the actual month
        datetime.now() - timedelta(days=30)  # One month Ago
    ]
    rates_diff = get_results(source, dates)
    print_results(*rates_diff, dates)

    insert_one(DataModel(
        timestamp=time.time(),
        today=rates_diff[0] or 0,
        five_days=rates_diff[1] or 0,
        first_day=rates_diff[2] or 0,
        one_month=rates_diff[3] or 0
    ))


if __name__ == "__main__":
    SystemExit(main())
