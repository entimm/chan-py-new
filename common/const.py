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
    M1 = auto()
    M5 = auto()
    M15 = auto()
    M30 = auto()
    M60 = auto()

    DAY = auto()
    WEEK = auto()
    MON = auto()

