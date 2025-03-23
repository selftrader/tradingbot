import { useEffect, useState } from "react";
const BASE_URL = process.env.REACT_APP_API_URL;
function TradeAnalytics({ userId }) {
    const [trades, setTrades] = useState([]);

    useEffect(() => {
        fetch(`${BASE_URL}/api/analytics?user_id=${userId}`)
            .then(response => response.json())
            .then(data => setTrades(data))
            .catch(error => console.error("Error fetching trade analytics:", error));
    }, [userId]);

    return (
        <div>
            <h2>Trade Analytics</h2>
            <table>
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Trade Type</th>
                        <th>Entry Price</th>
                        <th>Exit Price</th>
                        <th>Profit/Loss</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {trades.map((trade, index) => (
                        <tr key={index}>
                            <td>{trade.symbol}</td>
                            <td>{trade.trade_type}</td>
                            <td>₹{trade.entry_price}</td>
                            <td>{trade.exit_price === "Open Trade" ? "Open" : `₹${trade.exit_price}`}</td>
                            <td style={{ color: trade.profit_loss >= 0 ? "green" : "red" }}>
                                {trade.profit_loss === "Pending" ? "Pending" : `₹${trade.profit_loss}`}
                            </td>
                            <td>{trade.status}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default TradeAnalytics;
