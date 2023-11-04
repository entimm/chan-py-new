import abc
from typing import Iterable

from common.const import PeriodEnum


class AbsStockApi:
    def __init__(self, ticker, begin_date, end_date, period: PeriodEnum):
        self.ticker = ticker
        self.begin_date = begin_date
        self.end_date = end_date
        self.period = period

    @abc.abstractmethod
    def get_kl_data(self):
        pass