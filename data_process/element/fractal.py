import config
from data_process import chan_config
from data_process.element.bar_union import BarUnion
from data_process.const import FractalType


class Fractal:
    @staticmethod
    def check_valid_end(fractal_start: BarUnion, fractal_end: BarUnion):
        """
        检查2个分型是否可以连接成笔
        """
        # 两个分型须有一个是顶、一个是底,不能相同
        if Fractal.fractal_type_same(fractal_start, fractal_end):
            return False

        # 中间需要独立合并K线
        stroke_len = fractal_end.index - fractal_start.index
        if stroke_len < 4:
            return False

        if chan_config.stroke_check_break:
            return not Fractal.check_break(fractal_start, fractal_end)

        return True

    @staticmethod
    def check_break(fractal_start: BarUnion, fractal_end: BarUnion):
        """
        检查2个分型中间是否有k线破坏
        检查前面是否有因长度不够，而导致无法形成笔尾，然后后面的候选笔尾又无法higher_or_lower的
        """
        iter_bar_union = fractal_start
        while iter_bar_union.index < fractal_end.index:
            if fractal_start.fractal_type == FractalType.TOP:
                is_break = iter_bar_union.low < fractal_end.low
            else:
                is_break = iter_bar_union.high > fractal_end.high
            if is_break: return True
            iter_bar_union = iter_bar_union.next

        return False

    @staticmethod
    def same_type_fractal_growing(fractal1: BarUnion, fractal2: BarUnion):
        """
        fractal1先、fractal2后
        比较两个同为顶或同为底的2个分型，是否higher_or_lower
        """
        assert fractal1.fractal_type == fractal2.fractal_type
        if fractal1.fractal_type == FractalType.TOP and fractal1.high <= fractal2.high:
            return True
        if fractal1.fractal_type == FractalType.BOTTOM and fractal1.low >= fractal2.low:
            return True

        return False

    @staticmethod
    def fractal_type_same(fractal1: BarUnion, fractal2: BarUnion):
        return fractal1.fractal_type == fractal2.fractal_type
