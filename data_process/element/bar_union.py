from typing import List, Optional

from data_process.element.bar import Bar
from data_process.const import Direction, FractalType
from data_process.element.abs_bar import AbsBar


class BarUnion(AbsBar):
    def __init__(self, index, bar: Bar, direction=Direction.INIT, fractal_type=FractalType.NOTHING):
        self.start = bar.index
        self.end = bar.index
        self._high = bar.high
        self._low = bar.low

        self.direction: Direction = direction

        # 分型类型
        self.fractal_type = fractal_type
        # 分型时间
        self.fractal_index = 0
        # 分型值
        self.fractal_value = 0

        self._index = index

        self.next: Optional[BarUnion] = None

        self.bar_list: List[Bar] = [bar]

    def perform_union(self, bar: Bar):
        """
        执行合并操作
        """
        self.end = bar.index
        self.bar_list.append(bar)
        # 上涨趋势取双高
        if self.direction == Direction.UP:
            self._high = max(self._high, bar.high)
            self._low = max(self._low, bar.low)
        # 上涨趋势取双低
        if self.direction == Direction.DOWN:
            self._high = min(self._high, bar.high)
            self._low = min(self._low, bar.low)
        # 最开始的几根可以合并的k线无法定性趋势
        if self.direction == Direction.INIT:
            self._high = max(self._high, bar.high)
            self._low = min(self._low, bar.low)

    def get_key_pos(self):
        """
        根据趋势方向，取得其中关键K线的位置信息
        """
        if self.direction == Direction.UP:
            for bar in self.bar_list[::-1]:
                if self._high == bar.high:
                    return bar.index, bar.high

        if self.direction == Direction.DOWN:
            for bar in self.bar_list[::-1]:
                if self._low == bar.low:
                    return bar.index, bar.low

    def set_fractal(self, fractal_type: FractalType):
        self.fractal_type = fractal_type
        self.fractal_index, self.fractal_value = self.get_key_pos()

    def is_fractal(self):
        return self.fractal_type in [FractalType.TOP, FractalType.BOTTOM]

    def __str__(self):
        if self.fractal_type == FractalType.NOTHING:
            return f'【合K:{self.start}->{self.end}】'
        if self.fractal_type == FractalType.TOP:
            return f'【顶K:{self.fractal_index}】'
        if self.fractal_type == FractalType.BOTTOM:
            return f'【底K:{self.fractal_index}】'

    def __eq__(self, other):
        return self._index == other.index

    @property
    def index(self):
        return self._index

    @property
    def high(self):
        return self._high

    @property
    def low(self):
        return self._low
