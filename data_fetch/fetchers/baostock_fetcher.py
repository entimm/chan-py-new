import baostock as bs
from baostock.data.resultset import ResultData

import config
from common.const import AdjType, DataField, PeriodEnum
from data_fetch.fetcher import Fetcher


class BaostockFetcher(Fetcher):
    def __init__(self, ticker, start, end, period=PeriodEnum.D):
        super(BaostockFetcher, self).__init__(ticker, start, end, period)

    def get_kl_data(self):
        bs.login()

        adj_type_dict = {AdjType.QFQ: "2", AdjType.HFQ: "1", AdjType.NONE: "3"}
        rs: ResultData = bs.query_history_k_data_plus(
            code=self.ticker,
            start_date=self.start,
            end_date=self.end,
            adjustflag=adj_type_dict[config.adj_type],
            fields="date,open,high,low,close,volume",
            frequency=self.__convert_period(),
        )
        if rs.error_code != '0':
            raise Exception(rs.error_msg)
        while rs.error_code == '0' and rs.next():
            item = rs.get_row_data()
            info = {
                DataField.TIME: item[0],
                DataField.OPEN: item[1],
                DataField.HIGH: item[2],
                DataField.LOW: item[3],
                DataField.CLOSE: item[4],
                DataField.VOLUME: item[5],
            }
            yield info

        bs.logout()

    def __convert_period(self):
        _dict = {
            PeriodEnum.F5: '5',
            PeriodEnum.F15: '15',
            PeriodEnum.F30: '30',
            PeriodEnum.H: '60',

            PeriodEnum.D: 'd',
            PeriodEnum.W: 'w',
            PeriodEnum.M: 'm',
        }
        return _dict[self.period]
