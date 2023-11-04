import pandas as pd

import config
from common.const import DataField, PeriodEnum
from data_fetch.abs_stock_api import AbsStockApi


class LocalFetcher(AbsStockApi):
    def __init__(self, ticker, begin_date=None, end_date=None, period=PeriodEnum.DAY):
        super(LocalFetcher, self).__init__(ticker, begin_date, end_date, period)

    def get_kl_data(self):
        file_path = f"data/{config.local_data_file_name}.csv"
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
