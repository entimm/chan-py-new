import abc
from typing import Iterable

from common.const import PeriodEnum


class AbsStockApi:
    def __init__(self, code, begin_date, end_date, period: PeriodEnum):
        self.code = code
        self.begin_date = begin_date
        self.end_date = end_date
        self.period = period

    @abc.abstractmethod
    def get_kl_data(self):
        pass