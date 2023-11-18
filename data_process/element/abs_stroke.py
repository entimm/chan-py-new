from abc import abstractmethod

from data_process.const import Direction
from data_process.element.abs_bar import AbsBar


class AbsStroke(AbsBar):
    @property
    def len(self):
        return 0

    @property
    def direction(self):
        return Direction.INIT

    def high_fractal(self):
        if self.direction == Direction.UP:
            return self.fractal_end
        else:
            return self.fractal_start

    def low_fractal(self):
        if self.direction == Direction.UP:
            return self.fractal_start
        else:
            return self.fractal_end

    @property
    def fractal_start(self):
        return None

    @property
    def fractal_end(self):
        return None


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