import React, { useEffect, useState } from "react";
const WS_BASE_URL = process.env.WEBSOCKET_BASE_URL;
const TradeDashboard = ({ userId }) => {
    const [trades, setTrades] = useState([]);

    useEffect(() => {
        const socket = new WebSocket(`ws://${WS_BASE_URL}/ws/trade/${userId}`);

        socket.onmessage = (event) => {
            const tradeUpdate = JSON.parse(event.data);
            setTrades((prevTrades) => [tradeUpdate, ...prevTrades]);
        };

        return () => socket.close();
    }, [userId]);

    return (
        <div>
            <h2>Live Trades</h2>
            <ul>
                {trades.map((trade) => (
                    <li key={trade.trade_id}>
                        {trade.trade_type} {trade.quantity} shares of {trade.symbol} at ₹{trade.price} ({trade.status})
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default TradeDashboard;
