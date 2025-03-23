import { useEffect, useState } from "react";

function TradeSignals({ userId }) {
    const [signals, setSignals] = useState([]);

    useEffect(() => {
        const WS_BASE_URL = process.env.REACT_APP_WEBSOCKET_BASE_URL;
        const socket = new WebSocket(`{WS_BASE_URL}/ws/trade_signals?user_id=${userId}`);

        socket.onmessage = (event) => {
            setSignals(JSON.parse(event.data));
        };

        return () => socket.close();
    }, [userId]);

    return (
        <div>
            <h2>Live AI Trade Signals</h2>
            <table>
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Trade Type</th>
                        <th>Confidence (%)</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {signals.map((signal, index) => (
                        <tr key={index}>
                            <td>{signal.symbol}</td>
                            <td>{signal.trade_type}</td>
                            <td>{signal.confidence}%</td>
                            <td>{signal.status}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default TradeSignals;
