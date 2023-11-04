import abc

from common.const import PeriodEnum


class Fetcher:
    def __init__(self, ticker, start, end, period: PeriodEnum):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.period = period

    @abc.abstractmethod
    def get_kl_data(self) -> iter:
        pass
