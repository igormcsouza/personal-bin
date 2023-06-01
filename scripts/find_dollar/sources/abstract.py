from abc import ABC, abstractmethod
import datetime


class RetrieveRateAbstract(ABC):

    @abstractmethod
    def get_today(self) -> str:
        pass

    @abstractmethod
    def get_before(self, date: datetime.datetime) -> str:
        pass
