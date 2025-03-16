from brokers.zerodha_broker import ZerodhaBroker
from brokers.upstox_broker import UpstoxBroker
from brokers.dhan_broker import DhanBroker
from brokers.angel_broker import AngelBroker

class BrokerFactory:
    _brokers = {
        "zerodha": ZerodhaBroker,
        "upstox": UpstoxBroker,
        "dhan": DhanBroker,
        "angel": AngelBroker
    }

    @classmethod
    def get_broker(cls, broker_name: str, config: dict):
        if broker_name.lower() not in cls._brokers:
            raise ValueError(f"Unsupported broker: {broker_name}")

        broker_class = cls._brokers[broker_name.lower()]
        return broker_class(**config)
