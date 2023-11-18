from typing import Optional

from data_process.element.abs_stroke import AbsStroke
from data_process.element.bar_union import BarUnion
from data_process.const import FractalType, Direction
from logger import logger


class Stroke(AbsStroke):
    direction: Direction

    def __init__(self, index, fractal_start: BarUnion, fractal_end: Optional[BarUnion]):
        # 笔头
        self._fractal_start: BarUnion = fractal_start
        # 笔尾
        self._fractal_end: BarUnion = fractal_end
        # 长度
        self._len = 0
        if fractal_end is not None:
            self._len = fractal_end.index - fractal_start.index
        # 是否确认
        self.is_ok = False

        self._index = index

        self._direction = self.__cal_direction()

        # 暂存分型（辅助计算之用）
        self.stash_fractal: Optional[BarUnion] = None

        self.waiting_process = True

    def set_start(self, cur_fractal: BarUnion):
        """
        设置笔头
        """
        self._fractal_start = cur_fractal
        self._direction = self.__cal_direction()
        logger.info(f'{self}设置笔首{cur_fractal}')

    def set_end(self, cur_fractal: Optional[BarUnion]):
        """
        设置笔尾
        """
        self._fractal_end = cur_fractal
        self._len = 0 if cur_fractal is None else cur_fractal.index - self._fractal_start.index
        logger.info(f'{self}设置笔尾{cur_fractal}')

        self.waiting_process = True

    def __cal_direction(self):
        return Direction.UP if self._fractal_start.fractal_type == FractalType.BOTTOM else Direction.DOWN

    @property
    def high(self):
        return self.high_fractal().fractal_value

    @property
    def low(self):
        return self.low_fractal().fractal_value

    @property
    def len(self):
        return self._len

    @property
    def index(self):
        return self._index

    @property
    def direction(self):
        return self._direction

    @property
    def fractal_start(self):
        return self._fractal_start

    @property
    def fractal_end(self):
        return self._fractal_end

    def __str__(self):
        return f'【笔{self._index} 长度{self._len} 方向{self._direction.name} 两端:{self._fractal_start}->{self._fractal_end}】'
