import datetime

from forex_python.converter import CurrencyRates

from find_dollar.sources.abstract import RetrieveRateAbstract


class RetrieveRateForex(RetrieveRateAbstract):

    # Create a CurrencyRates object
    c = CurrencyRates()

    def get_today(self) -> str:
        return self.c.get_rate('USD', 'BRL')
 
    def get_before(self, date: datetime.datetime) -> str:
        return self.c.get_rate('USD', 'BRL', date)
