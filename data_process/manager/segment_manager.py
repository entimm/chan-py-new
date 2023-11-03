from typing import List

from data_process.const import SegmentStatus, Direction
from data_process.element.segment import Segment
from data_process.element.stroke import Stroke
from logger import logger


class SegmentManager:
    def __init__(self):
        self.list: List[Segment] = []

    def add_stroke(self, stroke: Stroke):
        logger.info(f'投喂笔给线段 {stroke}')
        if stroke.len == 0:
            return
        if len(self.list) == 0:
            self.appendWithStroke(stroke)
            return

        last_segment = self.list[-1]

        self.try_make_new_segment(last_segment, stroke)

    def try_make_new_segment(self, last_segment: Segment, stroke: Stroke):
        """
        投喂笔形成线段
        由于笔会生长，所以相同的笔会返回进来
        """
        if last_segment.stroke_list[-1].index == stroke.index:
            logger.info(f'线段同笔更新')

            # 笔生长时更新极值点,并可能触发笔破坏
            last_segment.update_vertex(stroke)
            self.handle_break(last_segment)

            return

        if last_segment.check_if_add(stroke):
            last_segment.add_stroke(stroke)

            # 线段变长后更新极值点,并可能触发笔破坏
            last_segment.update_vertex(stroke)
            self.handle_break(last_segment)

            return

        self.appendWithStroke(stroke)

    def appendWithStroke(self, stroke: Stroke):
        segment = Segment(len(self.list), stroke)

        logger.info(f'新增线段: {segment}')
        if len(self.list) >= 1:
            self.list[-1].is_ok = True
        self.list.append(segment)

    def handle_break(self, last_segment):
        """
        处理线段破坏
        """
        if last_segment.status == SegmentStatus.BREAK:
            if len(self.list) == 1:
                last_segment.rebase()
            if len(self.list) >= 2:
                self.list[-2].merge(last_segment)
                self.list.pop()
                # 合并过完如果存在反向突破，则拆分并继续与前一线段进行部分合并
                if len(self.list) >= 2:
                    self.try_split()

    def try_split(self):
        """
        根据反向的极值笔进行拆分
        """
        pre_segment = self.list[-2]
        last_segment = self.list[-1]
        if pre_segment.direction == Direction.UP:
            if last_segment.top_stroke.high_fractal().index != pre_segment.top_stroke.high_fractal().index and last_segment.top_stroke.high_fractal().fractal_value >= pre_segment.top_stroke.high_fractal().fractal_value:
                self.split_then_merge(pre_segment, last_segment, last_segment.top_stroke)
        if pre_segment.direction == Direction.DOWN:
            if last_segment.bottom_stroke.low_fractal().index != pre_segment.bottom_stroke.low_fractal().index and last_segment.bottom_stroke.low_fractal().fractal_value <= pre_segment.bottom_stroke.low_fractal().fractal_value:
                self.split_then_merge(pre_segment, last_segment, last_segment.bottom_stroke)
                logger.info(f'after split_then_merge 前{pre_segment} 后{last_segment}')

    def split_then_merge(self, pre_segment: Segment, last_segment: Segment, stroke: Stroke):
        """
        拆分后进行合并
        """
        logger.info(f'{pre_segment} split_then_merge {last_segment} 用 {stroke}')
        out_stroke_list: list[Stroke] = []
        in_stroke_list: list[Stroke] = []
        for item in last_segment.stroke_list:
            if item.index <= stroke.index:
                out_stroke_list.append(item)
            else:
                in_stroke_list.append(item)

        if len(out_stroke_list) > 0:
            pre_segment.stroke_list = pre_segment.stroke_list + out_stroke_list
            pre_segment.len = len(pre_segment.stroke_list)
            if pre_segment.direction == Direction.UP:
                pre_segment.top_stroke = last_segment.top_stroke
            if pre_segment.direction == Direction.DOWN:
                pre_segment.bottom_stroke = last_segment.bottom_stroke
            last_segment.status = SegmentStatus.MERGE
            last_segment.is_ok = False

        if len(in_stroke_list) > 0:
            last_segment.stroke_list = in_stroke_list
            last_segment.len = len(in_stroke_list)
            last_segment.status = SegmentStatus.SPLIT
        else:
            self.list.pop()



