from typing import List, Optional

from data_process.element.bar import Bar
from data_process.const import Direction, FractalType


class BarUnion:
    def __init__(self, bar: Bar, direction=Direction.INIT, fractal_type=FractalType.NOTHING):
        self.time_begin = bar.time
        self.time_end = bar.time
        self.high = bar.high
        self.low = bar.low

        self.direction: Direction = direction

        # 分型类型
        self.fractal_type = fractal_type
        # 分型时间
        self.fractal_time = 0
        # 分型值
        self.fractal_value = 0

        self.index = 0

        self.next: Optional[BarUnion] = None

        self.bar_list: List[Bar] = [bar]

    def perform_union(self, bar: Bar):
        """
        执行合并操作
        """
        self.time_end = bar.time
        self.bar_list.append(bar)
        # 上涨趋势取双高
        if self.direction == Direction.UP:
            self.high = max(self.high, bar.high)
            self.low = max(self.low, bar.low)
        # 上涨趋势取双低
        if self.direction == Direction.DOWN:
            self.high = min(self.high, bar.high)
            self.low = min(self.low, bar.low)
        # 最开始的几根可以合并的k线无法定性趋势
        if self.direction == Direction.INIT:
            self.high = max(self.high, bar.high)
            self.low = min(self.low, bar.low)

    def get_key_pos(self):
        """
        根据趋势方向，取得其中关键K线的位置信息
        """
        if self.direction == Direction.UP:
            for bar in self.bar_list[::-1]:
                if self.high == bar.high:
                    return bar.time, bar.high

        if self.direction == Direction.DOWN:
            for bar in self.bar_list[::-1]:
                if self.low == bar.low:
                    return bar.time, bar.low

    def set_fractal(self, fractal_type: FractalType):
        self.fractal_type = fractal_type
        self.fractal_time, self.fractal_value = self.get_key_pos()

    def is_fractal(self):
        return self.fractal_type in [FractalType.TOP, FractalType.BOTTOM]