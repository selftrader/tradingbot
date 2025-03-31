import json
import os
from sqlalchemy.orm import Session
from database.models import BrokerInstrument
from database.connection import SessionLocal, engine
from database.models import Base

Base.metadata.create_all(bind=engine)

UPSTOX_FILE_PATH = os.path.join("instruments", "upstox_instruments.json")

def should_include(inst):
    if inst.get("exchange") == "NSE":
        return True
    if inst.get("exchange") == "MCX" and "CRUDEOIL" in inst.get("trading_symbol", "").upper():
        return True
    if inst.get("exchange") == "BSE" and "SENSEX" in inst.get("trading_symbol", "").upper():
        return True
    return False


def load_upstox_instruments():
    if not os.path.exists(UPSTOX_FILE_PATH):
        print(f"❌ File not found: {UPSTOX_FILE_PATH}")
        return

    with open(UPSTOX_FILE_PATH, "r") as f:
        data = json.load(f)

    session: Session = SessionLocal()
    inserted = updated = skipped = 0

    for inst in data:
        if not should_include(inst):
            continue

        existing = session.query(BrokerInstrument).filter_by(instrument_key=inst["instrument_key"]).first()

        if existing:
            # Update if anything changes
            has_changes = (
                existing.symbol != inst.get("trading_symbol") or
                existing.name != inst.get("name") or
                existing.lot_size != inst.get("lot_size") or
                existing.tick_size != inst.get("tick_size")
            )
            if has_changes:
                existing.symbol = inst.get("trading_symbol")
                existing.name = inst.get("name")
                existing.exchange = inst.get("exchange")
                existing.segment = inst.get("segment")
                existing.instrument_type = inst.get("instrument_type")
                existing.isin = inst.get("isin")
                existing.lot_size = inst.get("lot_size")
                existing.tick_size = inst.get("tick_size")
                existing.security_type = inst.get("security_type")
                updated += 1
            else:
                skipped += 1
            continue

        session.add(BrokerInstrument(
            broker_name="Upstox",
            symbol=inst.get("trading_symbol"),
            name=inst.get("name"),
            exchange=inst.get("exchange"),
            segment=inst.get("segment"),
            instrument_type=inst.get("instrument_type"),
            isin=inst.get("isin"),
            lot_size=inst.get("lot_size"),
            tick_size=inst.get("tick_size"),
            instrument_key=inst.get("instrument_key"),
            security_type=inst.get("security_type"),
        ))
        inserted += 1

    session.commit()
    session.close()

    print(f"✅ Load complete: Inserted={inserted}, Updated={updated}, Skipped={skipped}")

if __name__ == "__main__":
    load_upstox_instruments()
