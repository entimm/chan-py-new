from chan.chan_const import Direction
from chan.element.abs_bar import AbsBar


class AbsStroke(AbsBar):
    def __init__(self, index):
        super().__init__(index)
        self._len = 0
        self._direction = Direction.INIT

    @property
    def len(self):
        return self._len

    @len.setter
    def len(self, value):
        self._len = value

    @property
    def direction(self):
        return self._direction

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