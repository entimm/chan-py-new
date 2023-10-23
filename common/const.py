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
