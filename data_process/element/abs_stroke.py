from abc import abstractmethod

from data_process.const import Direction
from data_process.element.abs_bar import AbsBar


class AbsStroke(AbsBar):
    @property
    def len(self):
        return 0

    @property
    def index(self):
        return 0

    @property
    def direction(self):
        return Direction.INIT

    @abstractmethod
    def high_fractal(self):
        pass

    @abstractmethod
    def low_fractal(self):
        pass

    @staticmethod
    def high_vertex_higher(pre_stroke: 'AbsStroke', last_stroke: 'AbsStroke'):
        same = last_stroke.high_fractal() == pre_stroke.high_fractal()
        growing = last_stroke.high >= pre_stroke.high

        return not same and growing

    @staticmethod
    def low_vertex_lower(pre_stroke: 'AbsStroke', last_stroke: 'AbsStroke'):
        same = last_stroke.low_fractal() == pre_stroke.low_fractal()
        growing = last_stroke.low <= pre_stroke.low

        return not same and growing

    @staticmethod
    def is_overlapping(pre_stroke: 'AbsStroke', stroke: 'AbsStroke'):
        assert pre_stroke.direction == stroke.direction
        if stroke.direction == Direction.UP:
            result = stroke.low - pre_stroke.high <= 0
        else:
            result = stroke.high - pre_stroke.low >= 0

        return result