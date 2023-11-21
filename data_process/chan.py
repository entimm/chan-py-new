from data_process.element.bar import Bar
from data_process.element.kline import Kline
from data_process.manager.bar_union_manager import BarUnionManager
from data_process.manager.segment_manager import SegmentManager
from data_process.manager.stroke_manager import StrokeManager
from logger import logger


class Chan:
    def __init__(self):
        self.data_list: list[Kline] = []

        self.bar_union_manager: BarUnionManager = BarUnionManager()
        self.stroke_manager: StrokeManager = StrokeManager()
        self.segment_manager: SegmentManager = SegmentManager()

    def load(self, kl_data_list: list):
        for kl_data in kl_data_list:
            self._add_kl(Kline(kl_data))

    def _add_kl(self, kline: Kline):
        self.data_list.append(kline)
        index = len(self.data_list) - 1
        logger.info(f"new_data: {self.data_list[index].time}")
        new_bar = Bar(index, kline)
        bar_union = self.bar_union_manager.add_bar(new_bar)
        if bar_union is not None:
            self.stroke_manager.add_fractal(bar_union)
            for stroke in self.stroke_manager.waiting_process_list():
                stroke.waiting_process = False
                self.segment_manager.add_stroke(stroke)

    def append(self, kl_data):
        self._add_kl(Kline(kl_data))

