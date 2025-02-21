from typing import Dict

from brokers.base_broker import BaseBroker, DhanBroker
from brokers.upstox_broker import UpstoxBroker


class BrokerFactory:
    @staticmethod
    def get_broker(broker_config: Dict) -> BaseBroker:
        broker_type = broker_config.get("broker_name", "").lower()
        
        if broker_type == "dhan":
            return DhanBroker(
                api_key=broker_config["api_key"],
                client_id=broker_config["client_id"]
            )
        elif broker_type == "upstox":
            return UpstoxBroker(
                api_key=broker_config["api_key"],
                secret_key=broker_config["secret_key"]
            )
        else:
            raise ValueError(f"Unsupported broker: {broker_type}")