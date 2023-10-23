from typing import Optional

from data_process.element.bar_union import BarUnion
from data_process.const import FractalType, Direction


class Stroke:
    direction: Direction

    def __init__(self, fractal_start: BarUnion, fractal_end: Optional[BarUnion]):
        # 笔头
        self.fractal_start: BarUnion = fractal_start
        # 笔尾
        self.fractal_end: BarUnion = fractal_end
        # 长度
        self.len = 0
        if fractal_end is not None:
            self.len = fractal_end.index - fractal_start.index
        # 是否确认
        self.is_ok = False

        self.index = 0

        self.direction = self.cal_direction()

        # 暂存分型（辅助计算之用）
        self.stash_fractal: Optional[BarUnion] = None

    def set_start(self, cur_fractal: BarUnion):
        """
        设置笔头
        """
        self.fractal_start = cur_fractal
        self.direction = self.cal_direction()

    def set_end(self, cur_fractal: Optional[BarUnion]):
        """
        设置笔尾
        """
        self.fractal_end = cur_fractal
        self.len = 0 if cur_fractal is None else cur_fractal.index - self.fractal_start.index

    def cal_direction(self):
        return Direction.UP if self.fractal_start.fractal_type == FractalType.BOTTOM else Direction.DOWN
