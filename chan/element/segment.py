from typing import Optional

from chan.const import Direction, SegmentStatus
from chan.element.abs_stroke import AbsStroke
from logger import logger


class Segment(AbsStroke):
    def __init__(self, index, stroke: AbsStroke):
        super().__init__(index)
        self.stroke_list: list[AbsStroke] = []

        self._index = index

        self.status = SegmentStatus.INIT

        # 含有至高点的笔
        self.top_stroke: Optional[AbsStroke] = None
        # 含有至低点的笔
        self.bottom_stroke: Optional[AbsStroke] = None

        # 是否确认
        self.is_ok = False

        # 是否是1F走势类型
        self.is_trend_1f = False

        logger.info(f'新线段诞生:{self}')
        self.add_stroke(stroke)

    def add_stroke(self, stroke: AbsStroke):
        logger.info(f'{self} add_stroke {stroke}')
        if self._len == 0:
            self._direction = stroke.direction
            self.append(stroke)
            return

        self.append(stroke)

    def merge(self, front_segment: 'Segment'):
        """
        将前面的线段全部合并到当前的线段
        """
        self.set_stroke_list(self.stroke_list + front_segment.stroke_list)

        # 如果前面的线段的至高至低点超过了当前的线段则进行相应的更新
        if front_segment.top_stroke.high >= self.top_stroke.high:
            self.top_stroke = front_segment.top_stroke
        if front_segment.bottom_stroke.low <= self.bottom_stroke.low:
            self.bottom_stroke = front_segment.bottom_stroke

        logger.info(f'{self} merge {front_segment}, 合并后尾笔:{self.stroke_list[-1]}')

        self.status = SegmentStatus.MERGE
        self.is_ok = False

    def set_stroke_list(self, stroke_list):
        self.stroke_list = stroke_list
        self._len = len(self.stroke_list)

        self.pivot()

    def rebase(self):
        """
        用于确定第一条线段的的开头位置
        如果存在反向突破就变基
        """
        rebase_stroke = self.top_stroke if self._direction == Direction.UP else self.bottom_stroke
        self.set_stroke_list([stroke for stroke in self.stroke_list if stroke.index > rebase_stroke.index])
        self._direction = self.stroke_list[0].direction

        self.bottom_stroke, self.top_stroke = self.stroke_list[0], self.stroke_list[-1]
        if self._direction == Direction.DOWN:
            self.bottom_stroke, self.top_stroke = self.top_stroke, self.bottom_stroke

        self.status = SegmentStatus.INIT

        logger.info(f'{self} rebase, start={self.stroke_list[0]}')

    def append(self, stroke: AbsStroke):
        self.stroke_list.append(stroke)
        self._len = len(self.stroke_list)

        self.pivot()

        self.update_vertex(stroke)

    def check_if_add(self, stroke: AbsStroke):
        """
        检测是否可以继续新增笔
        """
        if self._len < 3:
            return True

        # 一定是奇数个笔
        if self._len % 2 == 0:
            return True

        if self.status == SegmentStatus.INIT:
            return self.growing(stroke)

        if self.status == SegmentStatus.BREAK:
            return True

        return False

    def update_vertex(self, stroke: AbsStroke):
        """
        更新极点
        """
        if self._len == 1:
            self.top_stroke = stroke
            self.bottom_stroke = stroke
            return

        if AbsStroke.high_vertex_higher(self.top_stroke, stroke):
            self.set_top_stroke(stroke)
        if AbsStroke.low_vertex_lower(self.bottom_stroke, stroke):
            self.set_bottom_stroke(stroke)

    def set_top_stroke(self, stroke: AbsStroke):
        if self.top_stroke.index != stroke.index:
            if self._direction == Direction.UP:
                self.status = SegmentStatus.GROWING
                logger.info(f"{self} 延伸了 {self.top_stroke.high_fractal()} => {stroke.high_fractal()} | {self.top_stroke.index} => {stroke.index}")
            else:
                self.status = SegmentStatus.BREAK
                logger.info(f"{self} 破坏了 {self.top_stroke.high_fractal()} => {stroke.high_fractal()} | {self.top_stroke.index} => {stroke.index}")
            self.top_stroke = stroke

    def set_bottom_stroke(self, stroke: AbsStroke):
        if self.bottom_stroke.index != stroke.index:
            if self._direction == Direction.UP:
                self.status = SegmentStatus.BREAK
                logger.info(f"{self} 破坏了 {self.bottom_stroke.low_fractal()} => {stroke.low_fractal()} | {self.bottom_stroke.index} => {stroke.index}")
            else:
                self.status = SegmentStatus.GROWING
                logger.info(f"{self} 延伸了 {self.bottom_stroke.low_fractal()} => {stroke.low_fractal()} | {self.bottom_stroke.index} => {stroke.index}")
            self.bottom_stroke = stroke

    @staticmethod
    def top_vertex_higher(pre_segment: 'Segment', last_segment: 'Segment'):
        """
        前线段的正向极点比较后线段的反向极点（其实是同类型分型）
        """
        same_fractal = last_segment.top_stroke.high_fractal() == pre_segment.top_stroke.high_fractal()
        growing = last_segment.top_stroke.high >= pre_segment.top_stroke.high

        return not same_fractal and growing

    @staticmethod
    def bottom_vertex_lower(pre_segment: 'Segment', last_segment: 'Segment'):
        """
        前线段的正向极点比较后线段的反向极点（其实是同类型分型）
        """
        same_fractal = last_segment.bottom_stroke.low_fractal() == pre_segment.bottom_stroke.low_fractal()
        growing = last_segment.bottom_stroke.low <= pre_segment.bottom_stroke.low

        return not same_fractal and growing

    @staticmethod
    def merge_vertex(pre_segment: 'Segment', last_segment: 'Segment'):
        """
        前后线段合并极点
        """
        if pre_segment.direction == Direction.UP:
            pre_segment.top_stroke = last_segment.top_stroke
        if pre_segment.direction == Direction.DOWN:
            pre_segment.bottom_stroke = last_segment.bottom_stroke

    def __str__(self):
        stroke_desc = 'None'
        if len(self.stroke_list) > 0:
            stroke_desc = f'{self.stroke_list[0].index}->{self.stroke_list[-1].index}'

        return f"【线段{self._index} 方向 {self._direction.name} 长度{self._len} 状态:{self.status.name} 笔:{stroke_desc}】"

    def growing(self, stroke):
        # 反向极点
        back_vertex = self.bottom_stroke.low_fractal() if self._direction == Direction.UP else self.top_stroke.high_fractal()

        if self._direction == Direction.UP and stroke.direction == Direction.DOWN:
            return stroke.low <= back_vertex.fractal_value
        if self._direction == Direction.DOWN and stroke.direction == Direction.UP:
            return stroke.high >= back_vertex.fractal_value
        return True

    def pivot(self):
        if self._len >= 11:
            self.is_trend_1f = AbsStroke.is_overlapping(self.stroke_list[0], self.stroke_list[-1])

    @property
    def high(self):
        stroke = self.stroke_list[-1] if self._direction == Direction.UP else self.stroke_list[0]

        return stroke.high

    @property
    def low(self):
        stroke = self.stroke_list[0] if self._direction == Direction.UP else self.stroke_list[-1]

        return stroke.low

    def fractal_start(self):
        if self._direction == Direction.UP:
            return self.stroke_list[0].low_fractal()
        else:
            return self.stroke_list[0].high_fractal()

    def fractal_end(self):
        if self._direction == Direction.UP:
            return self.stroke_list[-1].high_fractal()
        else:
            return self.stroke_list[-1].low_fractal()
