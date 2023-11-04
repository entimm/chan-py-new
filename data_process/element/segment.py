from typing import Optional

from data_process.const import Direction, SegmentStatus
from data_process.element.stroke import Stroke
from logger import logger


class Segment:
    def __init__(self, index, stroke: Stroke):
        self.stroke_list: list[Stroke] = []

        self.index = index

        self.direction = Direction.INIT

        self.len = 0

        self.status = SegmentStatus.INIT

        # 含有至高点的笔
        self.top_stroke: Optional[Stroke] = None
        # 含有至低点的笔
        self.bottom_stroke: Optional[Stroke] = None

        self.add_stroke(stroke)

        # 是否确认
        self.is_ok = False

    def add_stroke(self, stroke: Stroke):
        logger.info(f'{self} add_stroke {stroke}')
        if self.len == 0:
            self.direction = stroke.direction
            self.append(stroke)
            return

        self.append(stroke)

    def merge(self, front_segment: 'Segment'):
        """
        将前面的线段全部合并到当前的线段
        """
        self.stroke_list = self.stroke_list + front_segment.stroke_list
        self.len = len(self.stroke_list)

        # 如果前面的线段的至高至低点超过了当前的线段则进行相应的更新
        if front_segment.top_stroke.high_fractal().fractal_value >= self.top_stroke.high_fractal().fractal_value:
            self.top_stroke = front_segment.top_stroke
        if front_segment.bottom_stroke.low_fractal().fractal_value <= self.bottom_stroke.low_fractal().fractal_value:
            self.bottom_stroke = front_segment.bottom_stroke

        logger.info(f'{self} merge {front_segment}, 合并后尾笔:{self.stroke_list[-1]}')

        self.status = SegmentStatus.MERGE
        self.is_ok = False

    def rebase(self):
        """
        用于确定第一条线段的的开头位置
        如果存在反向突破就变基
        """
        rebase_fractal = self.back_stroke()
        self.stroke_list = [stroke for stroke in self.stroke_list if stroke.index >= rebase_fractal.index]
        self.direction = self.stroke_list[0].direction
        self.len = len(self.stroke_list)

        self.status = SegmentStatus.INIT

        logger.info(f'{self} rebase, start={self.stroke_list[0]}')

    def append(self, stroke: Stroke):
        self.stroke_list.append(stroke)
        self.len = len(self.stroke_list)

        self.update_vertex(stroke)

    def check_if_add(self, stroke):
        """
        检测是否可以继续新增笔
        """
        if self.len < 3:
            return True

        # 一定是奇数个笔
        if self.len % 2 == 0:
            return True

        return False

    def update_vertex(self, stroke: Stroke):
        """
        更新极点
        """
        if self.len == 1:
            self.top_stroke = stroke
            self.bottom_stroke = stroke
            return

        if Stroke.high_vertex_higher(self.top_stroke, stroke):
            self.set_top_stroke(stroke)
        if Stroke.low_vertex_lower(self.bottom_stroke, stroke):
            self.set_bottom_stroke(stroke)

    def set_top_stroke(self, stroke: Stroke):
        if self.top_stroke.index != stroke.index:
            if self.direction == Direction.UP:
                self.status = SegmentStatus.GROWING
                logger.info(f"{self} 延伸了 {self.top_stroke.high_fractal()} => {stroke.high_fractal()} | {self.top_stroke.index} => {stroke.index}")
            else:
                self.status = SegmentStatus.BREAK
                logger.info(f"{self} 破坏了 {self.top_stroke.high_fractal()} => {stroke.high_fractal()} | {self.top_stroke.index} => {stroke.index}")
            self.top_stroke = stroke

    def set_bottom_stroke(self, stroke: Stroke):
        if self.bottom_stroke.index != stroke.index:
            if self.direction == Direction.UP:
                self.status = SegmentStatus.BREAK
                logger.info(f"{self} 破坏了 {self.bottom_stroke.low_fractal()} => {stroke.low_fractal()} | {self.bottom_stroke.index} => {stroke.index}")
            else:
                self.status = SegmentStatus.GROWING
                logger.info(f"{self} 延伸了 {self.bottom_stroke.low_fractal()} => {stroke.low_fractal()} | {self.bottom_stroke.index} => {stroke.index}")
            self.bottom_stroke = stroke

    def forward_stroke(self):
        """
        正向极点笔
        """
        return self.top_stroke if self.direction == Direction.UP else self.bottom_stroke

    def back_stroke(self):
        """
        反向极点笔
        """
        return self.bottom_stroke if self.direction == Direction.UP else self.top_stroke

    @staticmethod
    def top_vertex_higher(pre_segment: 'Segment', last_segment: 'Segment'):
        """
        前线段的正向极点比较后线段的反向极点（其实是同类型分型）
        """
        same_fractal = last_segment.top_stroke.high_fractal().index == pre_segment.top_stroke.high_fractal().index
        growing = last_segment.top_stroke.high_fractal().fractal_value >= pre_segment.top_stroke.high_fractal().fractal_value

        return not same_fractal and growing

    @staticmethod
    def bottom_vertex_lower(pre_segment: 'Segment', last_segment: 'Segment'):
        """
        前线段的正向极点比较后线段的反向极点（其实是同类型分型）
        """
        same_fractal = last_segment.bottom_stroke.low_fractal().index == pre_segment.bottom_stroke.low_fractal().index
        growing = last_segment.bottom_stroke.low_fractal().fractal_value <= pre_segment.bottom_stroke.low_fractal().fractal_value

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

        return f"【线段{self.index} 方向 {self.direction.name} 长度{self.len} 状态:{self.status.name} 笔:{stroke_desc}】"
