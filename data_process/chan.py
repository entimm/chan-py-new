import config
from data_fetch import manager
from data_fetch.fetcher import Fetcher
from data_process.element.bar import Bar
from data_process.manager.bar_union_manager import BarUnionManager
from data_process.manager.segment_manager import SegmentManager
from data_process.manager.stroke_manager import StrokeManager
from logger import logger


class Chan:
    def __init__(self, ticker, start, end, period):
        self.ticker = ticker
        self.period = period
        self.start = start
        self.end = end

        self.bar_union_manager: BarUnionManager = BarUnionManager()
        self.stroke_manager: StrokeManager = StrokeManager()
        self.segment_manager: SegmentManager = SegmentManager()

        self.data_list = []
        self.i = 0

        self.fetch()

    def fetch(self):
        fetcher_cls = manager.get_fetcher(config.data_src)
        fetcher: Fetcher = fetcher_cls(ticker=self.ticker, start=self.start, end=self.end, period=self.period)
        for kl_data in fetcher.get_kl_data():
            self.data_list.append(kl_data)

    def add_kl(self, kl_data):
        logger.info(f"新K线{self.data_list[self.i]['time']}")
        new_bar = Bar(kl_data)
        bar_union = self.bar_union_manager.add_bar(new_bar)
        if bar_union is not None:
            stroke = self.stroke_manager.add_fractal(bar_union)
            if stroke is not None:
                self.segment_manager.add_stroke(stroke)

    def load(self):
        while self.i <= config.step_skip:
            self.step_load()

    def step_load(self):
        if self.i >= len(self.data_list):
            return

        self.add_kl(self.data_list[self.i])
        self.i += 1
