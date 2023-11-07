import pandas as pd

import config
from common.const import DataField, PeriodEnum
from data_fetch.fetcher import Fetcher


class LocalFetcher(Fetcher):
    def __init__(self, ticker, start=None, end=None, period=PeriodEnum.D):
        super(LocalFetcher, self).__init__(ticker, start, end, period)

    def get_kl_data(self):
        file_path = f"data/kline/{config.local_data_file_name}-{self.period.name.lower()}.csv"
        df = pd.read_csv(file_path)

        for index, row in df.tail(config.kline_len).iterrows():
            yield {
                DataField.TIME: row["time"],
                DataField.OPEN: row["open"],
                DataField.HIGH: row["high"],
                DataField.LOW: row["low"],
                DataField.CLOSE: row["close"],
                DataField.VOLUME: row["volume"],
            }
