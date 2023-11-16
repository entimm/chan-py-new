import yfinance as yf

import config
from common.const import DataField, AdjType, PeriodEnum
from data_fetch.fetcher import Fetcher


class YfinanceFetcher(Fetcher):
    def __init__(self, ticker, start, end, period=PeriodEnum.D):
        super(YfinanceFetcher, self).__init__(ticker, start, end, period)

    def get_kl_data(self):
        adj_type_dict = {AdjType.QFQ: True, AdjType.HFQ: False, AdjType.NONE: None}
        ticker = yf.Ticker(self.ticker)
        intraday_data = ticker.history(
            start=self.start,
            end=self.end,
            actions=adj_type_dict[config.adj_type],
            interval=self.__convert_period(),
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

    def __convert_period(self):
        _dict = {
            PeriodEnum.F1: '1m',
            PeriodEnum.F5: '5m',
            PeriodEnum.F15: '15m',
            PeriodEnum.F30: '30m',
            PeriodEnum.H: '1h',

            PeriodEnum.D: '1d',
            PeriodEnum.W: '1wk',
            PeriodEnum.M: '1mo',
        }
        return _dict[self.period]
