import baostock as bs

import config
from common.const import AdjType, DataField, PeriodEnum
from data_fetch.abs_stock_api import AbsStockApi


class BaostockFetcher(AbsStockApi):
    def __init__(self, code, begin_date=None, end_date=None, period=PeriodEnum.DAY):
        super(BaostockFetcher, self).__init__(code, begin_date, end_date, period)

    def get_kl_data(self):
        bs.login()

        adj_type_dict = {AdjType.QFQ: "2", AdjType.HFQ: "1", AdjType.NONE: "3"}
        rs = bs.query_history_k_data_plus(
            code=self.code,
            start_date=self.begin_date,
            end_date=self.end_date,
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
            PeriodEnum.M5: '5',
            PeriodEnum.M15: '15',
            PeriodEnum.M30: '30',
            PeriodEnum.M60: '60',

            PeriodEnum.DAY: 'd',
            PeriodEnum.WEEK: 'w',
            PeriodEnum.MON: 'm',
        }
        return _dict[self.period]
