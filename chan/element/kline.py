class Kline:
    def __init__(self, kl_data: dict):
        self.time = kl_data['time']
        self.open = kl_data['open']
        self.high = kl_data['high']
        self.low = kl_data['low']
        self.close = kl_data['close']
        self.volume = kl_data['volume']