from enum import auto, Enum


class DataField:
    TIME = "time"
    OPEN = "open"
    HIGH = "high"
    LOW = "low"
    CLOSE = "close"
    VOLUME = "volume"


class AdjType(Enum):
    QFQ = auto()
    HFQ = auto()
    NONE = auto()


class PeriodEnum(Enum):
    F1 = auto()
    F5 = auto()
    F15 = auto()
    F30 = auto()

    H = auto()

    D = auto()
    W = auto()
    M = auto()
