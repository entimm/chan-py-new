from typing import List, Optional

from chan.element.abs_bar import AbsBar
from chan.element.bar_union import BarUnion
from chan.chan_const import CompareRelation, Direction, FractalType


class BarUnionManager:
    def __init__(self):
        self.list: List[BarUnion] = []

    def add_bar(self, new_bar: AbsBar):
        """
        投喂k线，生成合并k线，返回生成的分型
        """
        fractal: Optional[BarUnion] = None

        if len(self.list) == 0:
            self.append(BarUnion(len(self.list), new_bar))
        else:
            pre_bar_union = self.list[-1]
            self.try_union(pre_bar_union, new_bar)
            if pre_bar_union.is_fractal():
                fractal = pre_bar_union

        return fractal

    def append(self, bar_union: BarUnion):
        if len(self.list) >= 1:
            self.list[-1].next = bar_union

        self.list.append(bar_union)

    def try_union(self, pre_bar_union: BarUnion, cur_bar: AbsBar):
        """
        尝试合并
        """
        if cur_bar.index <= pre_bar_union.end: 
            return

        compare_relation = self.compare(pre_bar_union, cur_bar)

        if compare_relation == CompareRelation.CONTAIN or compare_relation == CompareRelation.CONTAINED:
            pre_bar_union.perform_union(cur_bar)
            return

        new_bar_union = BarUnion(len(self.list), cur_bar)

        if pre_bar_union.direction == Direction.UP:
            if compare_relation == CompareRelation.UP:
                new_bar_union.direction = Direction.UP
            if compare_relation == CompareRelation.DOWN:
                pre_bar_union.set_fractal(FractalType.TOP)
                new_bar_union.direction = Direction.DOWN

        if pre_bar_union.direction == Direction.DOWN:
            if compare_relation == CompareRelation.DOWN:
                new_bar_union.direction = Direction.DOWN
            if compare_relation == CompareRelation.UP:
                pre_bar_union.set_fractal(FractalType.BOTTOM)
                new_bar_union.direction = Direction.UP

        if pre_bar_union.direction == Direction.INIT:
            if compare_relation == CompareRelation.UP:
                pre_bar_union.direction = Direction.UP
                new_bar_union.direction = Direction.UP
            if compare_relation == CompareRelation.DOWN:
                pre_bar_union.direction = Direction.DOWN
                new_bar_union.direction = Direction.DOWN

        self.append(new_bar_union)

    def compare(self, bar_union: BarUnion, bar: AbsBar):
        """
        通过差值进行比较，进而得到bar_union和bar之间的关系
        """
        high_diff = bar.high - bar_union.high
        low_diff = bar.low - bar_union.low

        if high_diff > 0 and low_diff > 0:
            return CompareRelation.UP
        if high_diff < 0 and low_diff < 0:
            return CompareRelation.DOWN
        if high_diff >= 0 >= low_diff:
            return CompareRelation.CONTAIN
        if high_diff <= 0 <= low_diff:
            return CompareRelation.CONTAINED

    def bar_iter(self):
        for bar_union in self.list:
            yield from bar_union.bar_list

    def fractal_iter(self):
        for bar_union in self.list:
            if bar_union.is_fractal():
                yield bar_union
