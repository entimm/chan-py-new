from data_process.element.abs_bar import AbsBar
from data_process.kline import Kline


class Bar(AbsBar):
    def __init__(self, index, kline: Kline):
        self._index = index

        self._high = kline.high
        self._low = kline.low

    @property
    def index(self):
        return self._index

    @property
    def high(self):
        return self._high

    @property
    def low(self):
        return self._low
