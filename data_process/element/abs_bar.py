from abc import abstractmethod, ABC


class AbsBar(ABC):
    @property
    def high(self):
        return 0.0

    @property
    def low(self):
        return 0.0