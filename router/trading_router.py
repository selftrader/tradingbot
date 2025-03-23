from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.trade_monitor_service import TradeMonitorService
import logging

router = APIRouter()
trade_monitor = TradeMonitorService()

# Store active WebSocket connections
active_connections = []

@router.websocket("/ws/trades")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    logging.info("✅ New WebSocket connection established.")

    try:
        while True:
            trade_update = trade_monitor.get_latest_trade()
            if trade_update:
                for connection in active_connections:
                    await connection.send_json(trade_update)
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logging.info("🔌 WebSocket Disconnected.")
