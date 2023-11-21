import configparser
import os
from enum import Enum, auto

config = configparser.ConfigParser()
config.read('config.ini')

APP_PATH = os.path.dirname(os.path.dirname(__file__))

RESOURCES_PATH = os.path.join(APP_PATH, 'resources')

STOCK_META_FILE_PATH = os.path.join(RESOURCES_PATH, 'a_stock_meta_list.csv')
GNBK_FILE_PATH = os.path.join(RESOURCES_PATH, 'gnbk_list.csv')
ETF_FILE_PATH = os.path.join(RESOURCES_PATH, 'etf.csv')

TDX_PATH = config.get('tdx', 'app_path')


class PeriodEnum(Enum):
    F1 = auto()
    F5 = auto()
    F15 = auto()
    F30 = auto()
    D = auto()


TDX_FREQUENCY_MAP = {
    PeriodEnum.F1: 8,
    PeriodEnum.F5: 0,
    PeriodEnum.D: 9
}
