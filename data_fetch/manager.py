from enum import Enum, auto

class DataSrc(Enum):
    BAOSTOCK = auto()
    YFINANCE = auto()
    LOCAL = auto()
    FAKE = auto()


FETCHER_CLASSES = {
    DataSrc.BAOSTOCK: "BaostockFetcher",
    DataSrc.YFINANCE: "YfinanceFetcher",
    DataSrc.LOCAL: "LocalFetcher",
    DataSrc.FAKE: "FakeFetcher",
}


def get_stock_api(src):
    if src in FETCHER_CLASSES:
        cls_name = FETCHER_CLASSES[src]
        module = __import__(f"data_fetch.fetchers.{src.name.lower()}_fetcher", fromlist=[cls_name])
        return getattr(module, cls_name)

    if src.startswith("custom:"):
        package_info = src.split(":")[1]
        package_name, cls_name = package_info.split(".")
        module = __import__(f"data_api.apis.{package_name}", fromlist=[cls_name])
        return getattr(module, cls_name)

    raise Exception("src type not found")
