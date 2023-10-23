import yfinance as yf

import config
from common.const import DataField, AdjType
from data_fetch.abs_stock_api import AbsStockApi


class YfinanceFetcher(AbsStockApi):
    def __init__(self, code, begin_date=None, end_date=None):
        super(YfinanceFetcher, self).__init__(code, begin_date, end_date)

    def get_kl_data(self):
        adj_type_dict = {AdjType.QFQ: True, AdjType.HFQ: False, AdjType.NONE: None}
        ticker = yf.Ticker(self.code)
        intraday_data = ticker.history(
            start=self.begin_date,
            end=self.end_date,
            actions=adj_type_dict[config.adj_type],
        )

        for index, item in intraday_data.iterrows():
            yield {
                DataField.TIME: index.strftime('%Y-%m-%d'),
                DataField.OPEN: item["Open"],
                DataField.HIGH: item["High"],
                DataField.LOW: item["Low"],
                DataField.CLOSE: item["Close"],
                DataField.VOLUME: item["Volume"],
            }
