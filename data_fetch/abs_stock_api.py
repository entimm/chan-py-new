import abc
from typing import Iterable

class AbsStockApi:
    def __init__(self, code, begin_date, end_date):
        self.code = code
        self.begin_date = begin_date
        self.end_date = end_date

    @abc.abstractmethod
    def get_kl_data(self):
        pass