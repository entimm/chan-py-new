from common.common import PeriodEnum


def resample_kline(df, period_enum: PeriodEnum):
    resample_map = {
        PeriodEnum.F15: '15T',
        PeriodEnum.F30: '30T',
    }
    freq = resample_map[period_enum]
    df_15min = df.resample(freq, label='right', closed='right').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum',
    })

    return df_15min[df_15min['volume'] > 0]
