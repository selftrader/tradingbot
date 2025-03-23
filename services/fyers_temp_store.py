import time

_fyers_temp_store = {}

def store_fyers_credentials_temp(state: str, client_id: str, secret_key: str, redirect_uri: str):
    _fyers_temp_store[state] = {
        "client_id": client_id,
        "secret_key": secret_key,
        "redirect_uri": redirect_uri,
        "timestamp": time.time()
    }

def get_fyers_credentials_temp(state: str):
    return _fyers_temp_store.get(state)

def clear_fyers_credentials_temp(state: str):
    if state in _fyers_temp_store:
        del _fyers_temp_store[state]
