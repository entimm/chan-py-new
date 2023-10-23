from typing import List

import config
from data_process.element.bar_union import BarUnion
from data_process.const import FractalType
from data_process.element.fractal import Fractal
from data_process.element.stroke import Stroke


class StrokeManager:
    def __init__(self):
        self.list: List[Stroke] = []

        # 暂存与第一笔的笔头相反的分型 (辅助纠正第一笔的笔头之用)
        self.first_stroke_header_stash: List[BarUnion] = []

    def add_fractal(self, cur_fractal: BarUnion):
        """
        投喂分型生成笔
        """
        if cur_fractal.fractal_type not in [FractalType.TOP, FractalType.BOTTOM]:
            return

        if len(self.list) == 0:
            # 用第一个分型第一笔，有头无尾
            self.append(Stroke(cur_fractal, None))
            return

        last_stroke = self.list[-1]

        # 如果上一笔长度为0，这时肯定有头无尾
        if self.list[-1].len == 0:
            self.handle_first_stroke(last_stroke, cur_fractal)
            return

        self.try_make_new_stroke(last_stroke, cur_fractal)

    def handle_first_stroke(self, last_stroke, cur_fractal):
        """
        安排处理第一笔
        """
        # 如果笔头一开始就走higher_or_lower，说明笔头的类型需要纠正
        if Fractal.fractal_type_same(last_stroke.fractal_start, cur_fractal):
            if Fractal.same_type_fractal_growing(last_stroke.fractal_start, cur_fractal):
                if len(self.first_stroke_header_stash) >= 1:
                    last_stroke.set_start(self.first_stroke_header_stash.pop())
        else:
            # 把反向的分型先暂存上
            self.first_stroke_header_stash.append(cur_fractal)

        # 条件OK则把第一笔的笔尾设置上
        if Fractal.check_valid_end(last_stroke.fractal_start, cur_fractal):
            last_stroke.set_end(cur_fractal)

    def try_make_new_stroke(self, last_stroke: Stroke, cur_fractal: BarUnion):
        """
        尝试生成新笔
        """
        # 如果笔尾higher_or_lower，就换上bar_union为新笔尾
        if Fractal.fractal_type_same(last_stroke.fractal_end, cur_fractal):
            if Fractal.same_type_fractal_growing(last_stroke.fractal_end, cur_fractal):
                # 先判断是否有前面的关键分型，有就处理
                if config.stroke_fix_sure and last_stroke.stash_fractal is not None:
                    self.cancel_last_stroke(last_stroke.stash_fractal)
                    # 尝试生成下一笔
                    self.try_make_new_stroke(self.list[-1], cur_fractal)
                # 处理higher_or_lower分型
                # 笔顺势进行延伸
                else:
                    last_stroke.set_end(cur_fractal)
            return

        # 如果当前不能落新笔
        if not Fractal.check_valid_end(last_stroke.fractal_end, cur_fractal):
            # 上一笔的笔头移动判断及处理
            self.try_set_stash_fractal(last_stroke, cur_fractal)
            return

        # 落新笔
        last_stroke.is_ok = True
        self.append(Stroke(last_stroke.fractal_end, cur_fractal))

    def try_set_stash_fractal(self, last_stroke, cur_fractal):
        """
        尝试设置暂存的关键分型
        """
        if not config.stroke_fix_sure: return
        # 检查当前的bar_union和上一笔的笔头，进行高低比较
        if Fractal.fractal_type_same(last_stroke.fractal_start, cur_fractal):
            # 如果比上一笔的笔头higher_or_lower，则暂存当前分型
            # 为后续的变更实笔做准备，如果后面笔尾higher_or_lower，那么上一笔的笔头就该变了
            # last_stroke.stash_fractal不需要更新，自动丢弃
            if Fractal.same_type_fractal_growing(last_stroke.fractal_start, cur_fractal):
                if last_stroke.stash_fractal is None:
                    last_stroke.stash_fractal = cur_fractal
                return

    def append(self, stroke: Stroke):
        self.list.append(stroke)
        stroke.index = len(self.list) - 1

    def cancel_last_stroke(self, cur_fractal: BarUnion):
        """
        撤销上一笔
        变更上根实笔，变更实笔的笔尾，然后撤销其后的虚笔
        """
        assert len(self.list) >= 2

        self.list[-2].set_end(cur_fractal)
        self.list[-2].is_ok = False
        # 截断上根笔
        self.list.pop()
