from enum import Enum, auto


class Direction(Enum):
    INIT = auto()
    UP = auto()
    DOWN = auto()


class FractalType(Enum):
    TOP = auto()
    BOTTOM = auto()
    NOTHING = auto()


class CompareRelation(Enum):
    UP = auto()
    DOWN = auto()
    CONTAIN = auto()
    CONTAINED = auto()


class SegmentStatus(Enum):
    INIT = auto()
    BREAK = auto()
    GROWING = auto()
    MERGE = auto()
    FORCE = auto()
