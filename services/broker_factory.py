from typing import Dict, Type
from brokers.base_broker import BaseBroker
from brokers.upstox_broker import UpstoxBroker
from brokers.zerodha_broker import ZerodhaBroker
from brokers.dhan_broker import DhanBroker
from brokers.angel_broker import AngelBroker
from brokers.fyers_broker import FyersBroker

class BrokerFactory:
    _brokers = {
        "upstox": UpstoxBroker,
        "zerodha": ZerodhaBroker,
        "dhan": DhanBroker,
        "angel": AngelBroker,
        "fyers": FyersBroker
    }

    @classmethod
    def get_broker(cls, broker_name: str, config: Dict) -> BaseBroker:
        if broker_name not in cls._brokers:
            raise ValueError(f"Unsupported broker: {broker_name}")
        
        broker_class = cls._brokers[broker_name]
        return broker_class(**config)
