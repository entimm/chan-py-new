import math
from datetime import datetime

import pandas as pd
from mootdx.quotes import Quotes

from common.common import PeriodEnum, TDX_FREQUENCY_MAP
from common.data import local_tdx_reader
from common.price_calculate import resample_kline


def minutes_since_open():
    now = datetime.now()
    if now.weekday() in [5, 6]:
        return 0

    open_time = datetime(now.year, now.month, now.day, 9, 30)
    close_time = datetime(now.year, now.month, now.day, 16, 00)
    if open_time < now < close_time:
        diff = min(now, close_time) - open_time
        return math.ceil(diff.total_seconds() / 60)

    return 0


def fetch_local_data(reader, symbol, period):
    if period == PeriodEnum.F1:
        return reader.minute(symbol=symbol)
    elif period == PeriodEnum.F5:
        return reader.fzline(symbol=symbol)
    elif period == PeriodEnum.D:
        return reader.daily(symbol=symbol)


def realtime_whole_df(symbol, period_enum):
    base_period_enum = PeriodEnum.F1 if period_enum in [PeriodEnum.F15, PeriodEnum.F30] else period_enum

    frequency = TDX_FREQUENCY_MAP.get(base_period_enum)
    df = fetch_local_data(local_tdx_reader, symbol, base_period_enum)

    minutes = minutes_since_open()
    if minutes:
        if base_period_enum == PeriodEnum.D:
            offset = 5
        elif base_period_enum == PeriodEnum.F1:
            offset = minutes
        else:
            offset = minutes / 5
        client = Quotes.factory(market='std')
        real_time_df = client.bars(symbol=symbol, frequency=frequency, offset=offset)
        df = pd.concat([df, pd.DataFrame(real_time_df[['open', 'high', 'low', 'close', 'amount', 'volume']])], axis=0)

    if period_enum in [PeriodEnum.F15, PeriodEnum.F30]:
        df = resample_kline(df, period_enum)

    return df
