import config
from data_fetch import manager
from data_process.element.bar import Bar
from data_process.manager.bar_union_manager import BarUnionManager
from data_process.manager.stroke_manager import StrokeManager


class Chan:
    def __init__(self, ticker):
        self.ticker = ticker
        self.bar_union_manager: BarUnionManager = BarUnionManager()
        self.stroke_manager: StrokeManager = StrokeManager()

    def load(self, start, end):
        stockapi_cls = manager.get_stock_api(config.data_src)
        stockapi_instance = stockapi_cls(code=self.ticker, begin_date=start, end_date=end)
        for kl_data in stockapi_instance.get_kl_data():
            self.add_kl(kl_data)

    def add_kl(self, kl_data):
        new_bar = Bar(kl_data)
        bar_union = self.bar_union_manager.add_bar(new_bar)
        if bar_union is not None:
            self.stroke_manager.add_fractal(bar_union)
