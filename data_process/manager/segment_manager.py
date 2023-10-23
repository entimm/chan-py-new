from typing import List

from data_process.element.segment import Segment


class SegmentManager:
    def __init__(self):
        self.list: List[Segment] = []