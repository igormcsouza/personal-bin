from os import getenv
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

import requests
from forex_python.converter import CurrencyRates


class ProcessError(Exception):
    pass


class RetrieveRateAbstract(ABC):

    @abstractmethod
    def get_today(self) -> str:
        pass

    @abstractmethod
    def get_before(self, date: datetime) -> str:
        pass


class RetrieveRateForex(RetrieveRateAbstract):

    # Create a CurrencyRates object
    c = CurrencyRates()

    def get_today(self) -> str:
        return self.c.get_rate('USD', 'BRL')
 
    def get_before(self, date: datetime) -> str:
        return self.c.get_rate('USD', 'BRL', date)


class RetrieveRateOpenExchange(RetrieveRateAbstract):

    APP_ID = getenv("OPEN_EXCHANGE_APP_ID", "")
    BASE_URL = "https://openexchangerates.org/api/"
    HEADERS = {"accept": "application/json"}

    def __init__(self):
        if self.APP_ID == "":
            raise ProcessError(
                "There is no key configured on your Environment Variables"
                "Please, set an OPEN_EXCHANGE_APP_ID env var on you shell"
                "config file, or choose another source."
            )

    def get_today(self) -> str:
        response = requests.get(
            self.BASE_URL + f"latest.json?app_id={self.APP_ID}&base=USD&symbols=BRL", 
            headers=self.HEADERS
        )

        # breakpoint()

        resp_dict = response.json()

        if resp_dict.get("error", False):
            raise ProcessError(resp_dict["description"])

        return resp_dict["rates"]["BRL"]

    def get_before(self, date: datetime) -> str:
        response = requests.get(
            self.BASE_URL +
            f"historical/{date.strftime('%Y-%m-%d')}.json?app_id={self.APP_ID}&base=USD&symbols=BRL", 
            headers=self.HEADERS
        )

        resp_dict = response.json()

        if resp_dict.get("error", False):
            raise ProcessError(resp_dict["description"])

        return resp_dict["rates"]["BRL"]


def main():
    # Using OpenExchangeAPI source
    source = RetrieveRateOpenExchange()

    # Get today's exchange rate from USD to BRL
    today = datetime.now()
    today_rate = source.get_today()

    # Get the exchange rate from 5 days ago
    five_days_ago = datetime.now() - timedelta(days=5)
    five_days_ago_rate = source.get_before(five_days_ago)

    # Get the exchange rate from the first day of the current month
    first_day_of_month = datetime.now().replace(day=1)
    first_day_rate = source.get_before(first_day_of_month)

    # Get the exchange rate from exactly 1 month ago
    one_month_ago = datetime.now() - timedelta(days=30)
    one_month_ago_rate = source.get_before(one_month_ago)

    # Calculate the percentage difference between the rates
    five_days_ago_diff = ((today_rate - five_days_ago_rate) / five_days_ago_rate) * 100
    first_day_diff = ((today_rate - first_day_rate) / first_day_rate) * 100
    one_month_ago_diff = ((today_rate - one_month_ago_rate) / one_month_ago_rate) * 100

    # Print the results
    print(f">>> {today.strftime('%b %d, %Y')}")
    print(f">>> The exchange rate from USD to BRL today is BRL {today_rate:.2f}\n")

    # Calculate the maximum width of each column
    day_col_width = max(len("Day"), len(today.strftime('%b %d')), len(five_days_ago.strftime('%b %d')), len(first_day_of_month.strftime('%b %d')), len(one_month_ago.strftime('%b %d')))
    rate_col_width = max(len("Rate"), len("{:.2f}%".format(five_days_ago_diff)), len("{:.2f}%".format(first_day_diff)), len("{:.2f}%".format(one_month_ago_diff)), len("{:.2f}".format(today_rate)))

    # Print the results in a table format with fixed width columns
    print("| {}{} | {}{} |".format("Day".ljust(day_col_width), "", "Rate".rjust(rate_col_width), ""))
    print("|{}|{}|".format("-" * (day_col_width + 2), "-" * (rate_col_width + 2)))
    print("| {} | {} |".format("Today".ljust(day_col_width), "{:.2f}".format(today_rate).rjust(rate_col_width)))
    print("| {} | {} |".format(five_days_ago.strftime('%b %d').ljust(day_col_width), "{:.2f}%".format(five_days_ago_diff).rjust(rate_col_width)))
    print("| {} | {} |".format(first_day_of_month.strftime('%b %d').ljust(day_col_width), "{:.2f}%".format(first_day_diff).rjust(rate_col_width)))
    print("| {} | {} |".format(one_month_ago.strftime('%b %d').ljust(day_col_width), "{:.2f}%".format(one_month_ago_diff).rjust(rate_col_width)))

    return today_rate, five_days_ago_diff, first_day_diff, one_month_ago_diff


if __name__ == "__main__":
    SystemExit(main())

