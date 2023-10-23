import baostock as bs

import config
from common.const import AdjType, DataField
from data_fetch.abs_stock_api import AbsStockApi


class BaostockFetcher(AbsStockApi):
    def __init__(self, code, begin_date=None, end_date=None):
        super(BaostockFetcher, self).__init__(code, begin_date, end_date)

    def get_kl_data(self):
        bs.login()

        adj_type_dict = {AdjType.QFQ: "2", AdjType.HFQ: "1", AdjType.NONE: "3"}
        rs = bs.query_history_k_data_plus(
            code=self.code,
            start_date=self.begin_date,
            end_date=self.end_date,
            adjustflag=adj_type_dict[config.adj_type],
            fields="date,open,high,low,close,volume"
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
