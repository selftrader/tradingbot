import { useEffect, useState } from "react";
const WS_BASE_URL = process.env.WEBSOCKET_BASE_URL;

function LiveTradeMonitor({ userId }) {
    const [trades, setTrades] = useState([]);

    useEffect(() => {
        const socket = new WebSocket(`ws://{WS_BASE_URL}/ws/live_trades?user_id=${userId}`);

        socket.onmessage = (event) => {
            setTrades(JSON.parse(event.data));
        };

        return () => socket.close();
    }, [userId]);

    return (
        <div>
            <h2>Live Trade Monitoring</h2>
            <table>
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Trade Type</th>
                        <th>Entry Price</th>
                        <th>Current Price</th>
                        <th>Trailing Stop-Loss</th>
                    </tr>
                </thead>
                <tbody>
                    {trades.map((trade, index) => (
                        <tr key={index}>
                            <td>{trade.symbol}</td>
                            <td>{trade.trade_type}</td>
                            <td>₹{trade.entry_price}</td>
                            <td>₹{trade.current_price}</td>
                            <td>₹{trade.trailing_stop_loss}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default LiveTradeMonitor;
