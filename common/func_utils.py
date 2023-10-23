import pandas as pd


def is_time_valid(time_old: str, time_new: str):
    try:
        return pd.to_datetime(time_old).timestamp() < pd.to_datetime(time_new).timestamp()
    except ValueError:
        raise ValueError("无法解析时间字符串")
