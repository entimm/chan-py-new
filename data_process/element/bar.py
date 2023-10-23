from common.const import DataField


class Bar:
    def __init__(self, kl_data: dict):
        self.time = kl_data[DataField.TIME]
        self.open = kl_data[DataField.OPEN]
        self.high = kl_data[DataField.HIGH]
        self.low = kl_data[DataField.LOW]
        self.close = kl_data[DataField.CLOSE]
        self.volume = kl_data[DataField.VOLUME]
