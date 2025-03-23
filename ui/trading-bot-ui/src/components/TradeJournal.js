import { useEffect, useState } from "react";
const BASE_URL = process.env.REACT_APP_API_URL;
function TradeJournal({ userId }) {
    const [journal, setJournal] = useState([]);

    useEffect(() => {
        fetch(`${BASE_URL}/api/trade_journal?user_id=${userId}`)
            .then(response => response.json())
            .then(data => setJournal(data))
            .catch(error => console.error("Error fetching trade journal:", error));
    }, [userId]);

    return (
        <div>
            <h2>AI Trade Journal</h2>
            <table>
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Trade Type</th>
                        <th>AI Confidence (%)</th>
                        <th>Execution Status</th>
                    </tr>
                </thead>
                <tbody>
                    {journal.map((entry, index) => (
                        <tr key={index}>
                            <td>{entry.symbol}</td>
                            <td>{entry.trade_type}</td>
                            <td>{entry.ai_confidence}%</td>
                            <td>{entry.execution_status}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default TradeJournal;
