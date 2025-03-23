import json
import os
import tempfile
from datetime import datetime, timedelta

# Path to the temporary JSON file
_temp_json_file = os.path.join(tempfile.gettempdir(), "upstox_temp_store.json")


# Load JSON store
def _load_temp_store():
    if not os.path.exists(_temp_json_file):
        return {}
    try:
        with open(_temp_json_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print("[ERROR] Failed to load JSON:", e)
        return {}


# Save to JSON file
def _save_temp_store(store):
    try:
        with open(_temp_json_file, 'w') as f:
            json.dump(store, f, indent=4)
    except Exception as e:
        print("[ERROR] Failed to save JSON:", e)


# ✅ Store credentials using user_id (must be int)
def store_upstox_credentials_temp(user_id: int, client_id: str, client_secret: str, ttl: int = 300):
    expiry_timestamp = (datetime.utcnow() + timedelta(seconds=ttl)).timestamp()

    store = _load_temp_store()
    store[str(user_id)] = {
        "client_id": client_id,
        "client_secret": client_secret,
        "expires_at": expiry_timestamp
    }

    _save_temp_store(store)
    print(f"[INFO] Stored credentials for user_id={user_id}, expires_at={expiry_timestamp}")


# ✅ Get credentials if not expired
def get_upstox_credentials_temp(user_id: int):
    store = _load_temp_store()
    creds = store.get(str(user_id))  # Ensure key is string

    if not creds:
        print(f"[INFO] No credentials found for user_id={user_id}")
        return None

    expires_at = creds.get("expires_at")
    now_ts = datetime.utcnow().timestamp()

    if not expires_at or expires_at < now_ts:
        print(f"[INFO] Credentials expired for user_id={user_id}")
        clear_upstox_credentials_temp(user_id)
        return None

    print(f"[INFO] Credentials valid for user_id={user_id}")
    return creds


# ✅ Clear credentials manually
def clear_upstox_credentials_temp(user_id: int):
    store = _load_temp_store()
    if str(user_id) in store:
        del store[str(user_id)]
        _save_temp_store(store)
        print(f"[INFO] Cleared credentials for user_id={user_id}")


# 🔍 (Optional) Debug - list all entries
def list_all_temp_credentials():
    store = _load_temp_store()
    print("🔍 Stored Entries:")
    for user_id, creds in store.items():
        print(f"User ID: {user_id}")
        print(f"  Client ID:     {creds['client_id']}")
        print(f"  Client Secret: {creds['client_secret']}")
        print(f"  Expires At:    {datetime.utcfromtimestamp(creds['expires_at'])}")
        print("-" * 40)
