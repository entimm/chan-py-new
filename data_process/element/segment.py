from typing import Optional

from data_process.const import Direction, SegmentStatus
from data_process.element.stroke import Stroke


class Segment:
    def __init__(self, stroke: Stroke):
        self.stroke_list: list[Stroke] = []

        self.index = -1

        self.direction = Direction.INIT

        self.len = 0

        self.status = SegmentStatus.INIT

        # 含有至高点的笔
        self.top_stroke: Optional[Stroke] = None
        # 含有至低点的笔
        self.bottom_stroke: Optional[Stroke] = None

        self.add_stroke(stroke)

    def add_stroke(self, stroke: Stroke):
        print(f'{self} add_stroke {stroke}')
        if self.len == 0:
            self.direction = stroke.direction
            self.top_stroke = stroke
            self.bottom_stroke = stroke
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

        print(f'{self} merge {front_segment}, 合并后尾笔:{self.stroke_list[-1]}')

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

        print(f'{self} rebase, start={self.stroke_list[0]}')

    def append(self, stroke: Stroke):
        self.stroke_list.append(stroke)
        self.len = len(self.stroke_list)

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
        更新极值点
        """
        if stroke.high_fractal().index != self.top_stroke.high_fractal().index and stroke.high_fractal().fractal_value >= self.top_stroke.high_fractal().fractal_value:
            self.set_top_stroke(stroke)
        if stroke.low_fractal().index != self.bottom_stroke.low_fractal().index and stroke.low_fractal().fractal_value <= self.bottom_stroke.low_fractal().fractal_value:
            self.set_bottom_stroke(stroke)

    def set_top_stroke(self, stroke: Stroke):
        if self.top_stroke.index != stroke.index:
            if self.direction == Direction.UP:
                self.status = SegmentStatus.GROWING
                print(f"{self} 延伸了 {self.top_stroke.high_fractal()} => {stroke.high_fractal()} | {self.top_stroke.index} => {stroke.index}")
            else:
                self.status = SegmentStatus.BREAK
                print(f"{self} 破坏了 {self.top_stroke.high_fractal()} => {stroke.high_fractal()} | {self.top_stroke.index} => {stroke.index}")
            self.top_stroke = stroke

    def set_bottom_stroke(self, stroke: Stroke):
        if self.bottom_stroke.index != stroke.index:
            if self.direction == Direction.UP:
                self.status = SegmentStatus.BREAK
                print(f"{self} 破坏了 {self.bottom_stroke.low_fractal()} => {stroke.low_fractal()} | {self.bottom_stroke.index} => {stroke.index}")
            else:
                self.status = SegmentStatus.GROWING
                print(f"{self} 延伸了 {self.bottom_stroke.low_fractal()} => {stroke.low_fractal()} | {self.bottom_stroke.index} => {stroke.index}")
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

    def __str__(self):
        strock_desc = 'None'
        if len(self.stroke_list) > 0:
            strock_desc = f'{self.stroke_list[0].index}->{self.stroke_list[-1].index}'

        return f"【线段{self.index} 方向 {self.direction.name} 长度{self.len} 笔:{strock_desc}】"
