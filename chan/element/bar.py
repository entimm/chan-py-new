from chan.element.abs_bar import AbsBar
from chan.element.kline import Kline


class Bar(AbsBar):
    def __init__(self, index, kline: Kline):
        super().__init__(index)

        self._high = kline.high
        self._low = kline.low

    @property
    def high(self):
        return self._high

    @property
    def low(self):
        return self._low
