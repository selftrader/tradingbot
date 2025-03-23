import { useEffect, useState } from "react";
const WS_BASE_URL = process.env.WEBSOCKET_BASE_URL;
function LiveProfit({ userId }) {
    const [profitUpdates, setProfitUpdates] = useState([]);

    useEffect(() => {
        const socket = new WebSocket(`ws://${WS_BASE_URL}/ws/profit?user_id=${userId}`);

        socket.onmessage = (event) => {
            setProfitUpdates(JSON.parse(event.data));
        }; 

        return () => socket.close();
    }, [userId]);

    return (
        <div>
            <h2>Live Profit & Loss</h2>
            <table>
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Trade Type</th>
                        <th>Entry Price</th>
                        <th>Current Price</th>
                        <th>Profit/Loss</th>
                    </tr>
                </thead>
                <tbody>
                    {profitUpdates.map((update, index) => (
                        <tr key={index}>
                            <td>{update.symbol}</td>
                            <td>{update.trade_type}</td>
                            <td>₹{update.entry_price}</td>
                            <td>₹{update.current_price}</td>
                            <td style={{ color: update.profit_loss >= 0 ? "green" : "red" }}>
                                ₹{update.profit_loss}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default LiveProfit;
