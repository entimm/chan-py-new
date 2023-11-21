from abc import ABC


class AbsBar(ABC):
    def __init__(self, index):
        self._index = index

    @property
    def index(self):
        return self._index

    @property
    def high(self):
        return 0.0

    @property
    def low(self):
        return 0.0
