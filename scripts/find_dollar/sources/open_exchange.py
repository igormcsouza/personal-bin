from os import getenv
import datetime

import requests

from find_dollar.utils import ProcessError
from find_dollar.sources.abstract import RetrieveRateAbstract


class RetrieveRateOpenExchange(RetrieveRateAbstract):

    APP_ID = getenv("OPEN_EXCHANGE_APP_ID", "")
    BASE_URL = "https://openexchangerates.org/api/"
    HEADERS = {"accept": "application/json"}

    def __init__(self, APP_ID=None):
        if APP_ID:
            self.APP_ID = APP_ID

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

    def get_before(self, date: datetime.datetime) -> str:
        response = requests.get(
            self.BASE_URL +
            f"historical/{date.strftime('%Y-%m-%d')}.json?app_id={self.APP_ID}&base=USD&symbols=BRL", 
            headers=self.HEADERS
        )

        resp_dict = response.json()

        if resp_dict.get("error", False):
            raise ProcessError(resp_dict["description"])

        return resp_dict["rates"]["BRL"]
