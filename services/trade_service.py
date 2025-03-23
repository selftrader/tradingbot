from core.websockets import manager

async def execute_trade(order_id: int):
    """
    Simulates trade execution and notifies clients in real-time.
    """
    # Simulating order execution (Replace this with actual broker API logic)
    trade_status = "FILLED"  # Example status
    trade_info = {
        "order_id": order_id,
        "status": trade_status,
        "message": f"Trade {order_id} executed successfully!"
    }
    
    # 🚀 Notify all connected WebSocket clients
    await manager.broadcast(trade_info)
    
    return trade_info
