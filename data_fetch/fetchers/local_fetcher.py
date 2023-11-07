import pandas as pd

import config
from common.const import DataField, PeriodEnum
from data_fetch.fetcher import Fetcher


class LocalFetcher(Fetcher):
    def __init__(self, ticker, start=None, end=None, period=PeriodEnum.D):
        super(LocalFetcher, self).__init__(ticker, start, end, period)

    def get_kl_data(self):
        file_path = f"data/{config.local_data_file_name}-{self.period.name.lower()}.csv"
        df = pd.read_csv(file_path)

        for index, row in df.tail(config.kline_len).iterrows():
            yield {
                DataField.TIME: row["Date"],
                DataField.OPEN: row["Open"],
                DataField.HIGH: row["High"],
                DataField.LOW: row["Low"],
                DataField.CLOSE: row["Close"],
                DataField.VOLUME: row["Volume"],
            }
